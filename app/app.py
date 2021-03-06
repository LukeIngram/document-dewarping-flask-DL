#   MIT License
#
#   Copyright (c) 2022 Luke Ingram
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#   
#   app.py

from flask import Flask, render_template,request,redirect,url_for,abort,send_from_directory,flash
from werkzeug.utils import secure_filename 
import os 
from scripts.verify import *
import scripts.main as converter
from pathlib import Path


app = Flask(__name__)
app.config.from_pyfile('keys/config.py')


@app.route("/",methods=['GET'])
def index(): 
    return render_template("index.html")


@app.route("/",methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    fname = secure_filename(file.filename)
    if fname != '': 
        file_ext = os.path.splitext(fname)[1]
        if file_ext != validate_image(file.stream,file_ext):
            flash("Unsupported File. Supported Types: (png, jpg, jpeg)")
            return redirect(url_for('index'))
        fpath = os.path.join(app.config["UPLOAD_PATH"],fname)
        file.save(fpath)
        flash("File Successfully Uploaded. Evaluating your submission...")
        sterilize_img(fpath)
        flash("\nConverting you image now. Your Download will Begin Shortly.")
        outgoing = convertImg(fpath)
        if outgoing == None: 
            flash("\nConversion Unsuccessful. Please Try a Different File.")
            return redirect(url_for('index'))
    return redirect(url_for('download',filename=outgoing))

def convertImg(filename): 
    if os.path.exists(filename):
        if converter.main(filename,app.config["OUTBOX_PATH"],True)[0] == 0:
            return os.path.splitext(os.path.basename(filename))[0] + '.pdf'
    return None

@app.route("/outbox/<filename>")
def download(filename): 
    try:
        return send_from_directory(app.config['OUTBOX_PATH'],filename,as_attachment=True)
    except FileNotFoundError:
        abort(500)

@app.route("/display/<filename>")
def display(filename): 
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__": 
    app.run(debug=True,port=5001)