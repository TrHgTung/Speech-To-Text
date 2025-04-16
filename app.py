import os
from flask import Flask, render_template, request, send_file, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime
from pydub.silence import split_on_silence

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def format_time(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"


def split_audio_by_time(audio, chunk_length_ms=40000):
    """Chia nhỏ file âm thanh theo thời lượng cố định (ms)."""
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    return chunks

def split_audio_by_silence(audio, min_silence_len=1000, silence_thresh=-40):
    """
    Chia nhỏ file âm thanh dựa trên khoảng lặng.
    - min_silence_len: độ dài tối thiểu của khoảng lặng để chia (ms)
    - silence_thresh: ngưỡng dBFS để coi là khoảng lặng
    """
    chunks = split_on_silence(audio, 
                               min_silence_len=min_silence_len, 
                               silence_thresh=audio.dBFS + silence_thresh,
                               keep_silence=300)
    return chunks

def convert_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + "_full.wav"
        audio.export(wav_path, format="wav")

        sound = AudioSegment.from_wav(wav_path)
        chunks = split_audio_by_time(sound, chunk_length_ms=40000)  # 40s mỗi đoạn

        final_text = ""
        for i, chunk in enumerate(chunks):
            start_time = i * 40  # 40s mỗi đoạn
            end_time = (i + 1) * 40
            start_str = format_time(start_time)
            end_str = format_time(end_time)

            chunk_path = f"{file_path}_chunk{i}.wav"
            chunk.export(chunk_path, format="wav")

            final_text += f"[{start_str} - {end_str}]\n"
            with sr.AudioFile(chunk_path) as source:
                try:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
                    final_text += text.strip() + "\n\n"
                except sr.UnknownValueError:
                    final_text += "[Không nhận diện được đoạn này]\n\n"
                except sr.RequestError:
                    final_text += "[Lỗi kết nối tới Google API]\n\n"
                except Exception as e:
                    final_text += f"[Lỗi khi xử lý đoạn {i}: {e}]\n\n"

            os.remove(chunk_path)

        os.remove(wav_path)
        return final_text.strip()

    except Exception as e:
        return f"Lỗi khi xử lý âm thanh: {e}"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/record")
def record():
    return render_template("record.html")


@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "audio_file" in request.files:
        file = request.files["audio_file"]
        if file.filename:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            result_text = convert_audio(filepath)

            txt_filename = datetime.now().strftime("result_%Y%m%d_%H%M%S.txt")
            txt_path = os.path.join(app.config["UPLOAD_FOLDER"], txt_filename)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result_text)

            return jsonify({"success": True, "download_url": f"/download/{txt_filename}"})

    return jsonify({"success": False, "message": "Không có file được tải lên."})


@app.route("/upload-silence", methods=["GET", "POST"])
def upload_by_silence():
    if request.method == "POST":
        if "audio_file" in request.files:
            file = request.files["audio_file"]
            if file.filename:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                audio = AudioSegment.from_file(filepath)
                chunks = split_audio_by_silence(audio)

                recognizer = sr.Recognizer()
                final_text = ""
                current_time_ms = 0

                for i, chunk in enumerate(chunks):
                    duration_ms = len(chunk)
                    start_sec = current_time_ms // 1000
                    end_sec = (current_time_ms + duration_ms) // 1000
                    start_str = format_time(start_sec)
                    end_str = format_time(end_sec)

                    chunk_path = f"{filepath}_silence_chunk{i}.wav"
                    chunk.export(chunk_path, format="wav")

                    final_text += f"[{start_str} - {end_str}]\n"
                    with sr.AudioFile(chunk_path) as source:
                        try:
                            audio_data = recognizer.record(source)
                            text = recognizer.recognize_google(audio_data, language="vi-VN")
                            final_text += text.strip() + "\n\n"
                        except sr.UnknownValueError:
                            final_text += "[Không nhận diện được đoạn này]\n\n"
                        except sr.RequestError:
                            final_text += "[Lỗi kết nối tới Google API]\n\n"
                        except Exception as e:
                            final_text += f"[Lỗi khi xử lý đoạn {i}: {e}]\n\n"

                    os.remove(chunk_path)
                    current_time_ms += duration_ms


                txt_filename = datetime.now().strftime("result_silence_%Y%m%d_%H%M%S.txt")
                txt_path = os.path.join(app.config["UPLOAD_FOLDER"], txt_filename)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(final_text)

                return jsonify({"success": True, "download_url": f"/download/{txt_filename}"})

    return render_template("upload_silence.html")


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
