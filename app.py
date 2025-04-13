import os
from flask import Flask, render_template, request, send_file, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def convert_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + "_full.wav"
        audio.export(wav_path, format="wav")

        sound = AudioSegment.from_wav(wav_path)
        chunks = split_on_silence(
            sound,
            min_silence_len=700,
            silence_thresh=sound.dBFS - 14,
            keep_silence=500
        )

        final_text = ""
        total_chunks = len(chunks)

        for i, chunk in enumerate(chunks):
            audio_chunk_path = f"{file_path}_chunk{i}.wav"
            chunk.export(audio_chunk_path, format="wav")
            with sr.AudioFile(audio_chunk_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
                    final_text += text.strip() + "\n\n"
                except sr.UnknownValueError:
                    final_text += "[Không nhận diện được đoạn này]\n\n"
                except sr.RequestError:
                    return "Lỗi kết nối tới dịch vụ nhận dạng."
            os.remove(audio_chunk_path)

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


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
