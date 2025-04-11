import os
from flask import Flask, render_template, request, send_file
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_audio(file_path):
    recognizer = sr.Recognizer()
    # audio = AudioSegment.from_file(file_path)
    # wav_path = file_path.rsplit(".", 1)[0] + ".wav"
    # audio.export(wav_path, format="wav")
    # audio = AudioSegment.from_file(file_path, format="webm")
    audio = AudioSegment.from_file(file_path) if file_path.endswith(".webm") else AudioSegment.from_file(file_path)
    wav_path = file_path.rsplit(".", 1)[0] + ".wav"
    audio.export(wav_path, format="wav")


    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="vi-VN")
            return text
        except sr.UnknownValueError:
            return "Không thể nhận dạng giọng nói."
        except sr.RequestError:
            return "Lỗi khi kết nối tới dịch vụ nhận dạng."

@app.route("/", methods=["GET", "POST"])
def index():
    result_text = ""
    if request.method == "POST":
        if "audio_file" in request.files:
            file = request.files["audio_file"]
            if file.filename != "":
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                result_text = convert_audio(filepath)

                # Lưu file .txt
                txt_filename = datetime.now().strftime("result_%Y%m%d_%H%M%S.txt")
                txt_path = os.path.join(app.config["UPLOAD_FOLDER"], txt_filename)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(result_text)
                return send_file(txt_path, as_attachment=True)

    return render_template("index.html", result_text=result_text)

if __name__ == "__main__":
    app.run(debug=True)
