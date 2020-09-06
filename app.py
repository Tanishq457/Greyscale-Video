from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import os

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

import filetype

from converttogreyscale import  *

def send_mail(send_from, send_to, subject, text, files=None,
              server="smtp.gmail.com:587"):
    # assert isinstance(send_to, list)
    # msg = 'There was a terrible error that occured and I wanted you to know!'

    msg = MIMEMultipart()
    # msg['From'] = send_from
    # msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    username = 'bhalla.tanishq2000'
    password = '2Rqk5QvgT'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.send_message(msg=msg, from_addr=send_from, to_addrs=send_to)
    # server.sendmail(send_from, send_to, msg)
    server.quit()
    
app = Flask(__name__)

UPLOAD_FOLDER = r'.'
sender_email = "bhalla.tanishq2000@gmail.com"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'fwegiylcg'

def allowed_file(filename):
    return '.' in filename

@app.route('/')
def upload_file():
   return render_template('home.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
       
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        flash('Hi')
        
        if filetype.guess(f).mime.split('/')[0] != 'video':
            flash('Given file is not a video file. Please give a video file.')
            return redirect(request.url)
        

        fileName = secure_filename(f.filename)

        f.save(fileName)
        fps, width, height = createFrames(fileName)
        fileName2 = combineGreyFrames(fileName, width, height, fps)


        send_mail(sender_email, sender_email, 'Hi', 'Hi There', [fileName])
        os.remove(fileName)
        os.remove(fileName2)
        return 'File Emailed Successfully'
    

if __name__ == '__main__':
   app.run(debug = True)