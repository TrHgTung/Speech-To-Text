import os
from flask import Flask, render_template, request, send_file
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def convert_audio(file_path):
#     recognizer = sr.Recognizer()

#     try:
#         audio = AudioSegment.from_file(file_path)

#         if len(audio) > 60000:
#             audio = audio[:60000]

#         wav_path = file_path.rsplit(".", 1)[0] + ".wav"
#         audio.export(wav_path, format="wav")

#         with sr.AudioFile(wav_path) as source:
#             audio_data = recognizer.record(source)

#             try:
#                 text = recognizer.recognize_google(audio_data, language="vi-VN")
#                 return text
#             except sr.UnknownValueError:
#                 return "Không thể nhận dạng giọng nói."
#             except sr.RequestError:
#                 return "Lỗi kết nối tới dịch vụ nhận dạng."
#     except Exception as e:
#         return f"Lỗi khi xử lý âm thanh: {e}"

def convert_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(file_path)
        chunk_length_ms = 60000  # 60 giây
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

        final_text = ""

        for index, chunk in enumerate(chunks):
            chunk_path = f"{file_path.rsplit('.', 1)[0]}_chunk{index}.wav"
            chunk.export(chunk_path, format="wav")

            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
                    final_text += text + " "
                except sr.UnknownValueError:
                    final_text += "[Không nhận diện được đoạn này] "
                except sr.RequestError:
                    return "Lỗi kết nối tới dịch vụ nhận dạng."

            os.remove(chunk_path)

        return final_text.strip()

    except Exception as e:
        return f"Lỗi khi xử lý âm thanh: {e}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
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

                return send_file(txt_path, as_attachment=True)
    return render_template("upload.html")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False, host="0.0.0.0", port=10000)
