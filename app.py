import sys, os, shutil
from os.path import basename

import smtplib


from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import filetype

from converttogreyscale import combineGreyFrames, createFrames


def send_mail(
    send_from, send_to, subject, text, files=None, server="smtp.gmail.com:587"
):
    msg = MIMEMultipart()
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    username = "bhalla.tanishq2000"
    password = "2Rqk5QvgT"
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.send_message(msg=msg, from_addr=send_from, to_addrs=send_to)
    # server.sendmail(send_from, send_to, msg)
    server.quit()


app = Flask(__name__)

UPLOAD_FOLDER = "."
SENDER_EMAIL = "bhalla.tanishq2000@gmail.com"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

'''Home Page of Application'''
@app.route("/")
def upload_file():
    return render_template("home.html")


'''Upload point of Application'''
@app.route("/upload", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":

        if "file" not in request.files:
            return "No file part"
        f = request.files["file"]
        if f.filename == "":
            return "No selected file"

        fileName = secure_filename(f.filename)

        f.save(fileName)
        if not filetype.video_match("./" + fileName):
            return "Given file is not a video file. Please give a video file."
        print('wegyifbcwe::' + str(request.form['name']), file=sys.stderr)
        TO_EMAIL = request.form['name']
        output = createFrames(fileName)
        print("output: " + str(output), file=sys.stderr)
        if output == None:
            shutil.rmtree("./temp")
            return "Error"
        fps, width, height = output
        fileName2 = combineGreyFrames(fileName, width, height, fps)

        send_mail(SENDER_EMAIL, TO_EMAIL, "Hi", "Hi There", [fileName2])
        os.remove(fileName)
        os.remove(fileName2)
        return "File Emailed Successfully"
    return "No File/Email given"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
