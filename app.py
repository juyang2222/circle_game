import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import time


app = Flask(__name__)

UPLOAD_FOLDER = "static/images/uploaded_image"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    uploaded_image = None
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = int(time.time())  # 현재 시간을 정수형으로 가져오기
            new_filename = f"{timestamp}_{filename}"  # 타임스탬프와 원래 파일 이름 조합

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
            file.save(file_path)

            # 업로드된 이미지 경로 설정
            uploaded_image = url_for(
                "static", filename=f"images/uploaded_image/{filename}"
            )

    return render_template("index.html", uploaded_image=uploaded_image)


@app.route("/start-game")
def start_game():
    uploaded_files = os.listdir(app.config["UPLOAD_FOLDER"])

    if uploaded_files:
        # 타임스탬프를 기준으로 파일 이름을 추출하고 정렬
        # 파일 이름 예시: "timestamp_filename.png"
        uploaded_files.sort(
            key=lambda x: os.path.getmtime(
                os.path.join(app.config["UPLOAD_FOLDER"], x)
            ),
            reverse=True,
        )

        # 가장 최근 파일 선택
        most_recent_file = uploaded_files[0]  # 최신 파일
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], most_recent_file)

        try:
            # game.py 실행, 경로를 인수로 전달
            subprocess.Popen(["python", "game.py", file_path])
            return "게임이 시작됩니다."
        except Exception as e:
            return f"게임 실행 중 오류 발생: {e}"
    else:
        return "업로드된 이미지가 없습니다."


if __name__ == "__main__":
    app.run(debug=False)
