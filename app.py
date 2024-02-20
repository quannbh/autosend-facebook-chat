from flask import Flask, render_template, request, redirect, url_for
from fbchat import Client
from fbchat.models import *

app = Flask(__name__)

def gui_tin_nhan(ten_tai_khoan, mat_khau, id_nguoi_nhan_list, noi_dung_tin_nhan_list):
    client = Client(ten_tai_khoan, mat_khau)

    try:
        for id_nguoi_nhan in id_nguoi_nhan_list:
            for noi_dung_tin_nhan in noi_dung_tin_nhan_list:
                # Gửi tin nhắn
                client.send(Message(text=noi_dung_tin_nhan), thread_id=id_nguoi_nhan, thread_type=ThreadType.USER)
        return True
    except Exception as e:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gui_tin_nhan", methods=["POST"])
def send_message():
    ten_tai_khoan_facebook = request.form.get("email")
    mat_khau_facebook = request.form.get("password")
    id_nguoi_nhan = request.form.get("recipient_id")
    noi_dung_tin_nhan = request.form.get("message")

    # Chia các nội dung tin nhắn thành các dòng riêng biệt
    noi_dung_tin_nhan_list = noi_dung_tin_nhan.split("\n")

    # Chia các người nhận thành danh sách riêng biệt
    id_nguoi_nhan_list = id_nguoi_nhan.split(",")

    # Gửi nhiều tin nhắn tới nhiều người nhận
    if gui_tin_nhan(ten_tai_khoan_facebook, mat_khau_facebook, id_nguoi_nhan_list, noi_dung_tin_nhan_list):
        success_message = "Đã gửi tin nhắn thành công!"
    else:
        success_message = "Có lỗi xảy ra trong quá trình gửi tin nhắn."

    return success_message

@app.route("/success")
def success():
    message = request.args.get('message', default="", type=str)
    return render_template("success.html", message=message)

# Thêm đoạn mã sau để chạy ứng dụng với Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
