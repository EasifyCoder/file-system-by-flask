import os
from flask import Flask
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder="templates")
Bootstrap(app)

# 上传的文件夹名称
UPLOAD_FOLDER = 'upload'
# 上传的文件夹路径
UPLOAD_PATH = os.path.join(app.root_path,'upload')
# 允许上传的文件格式
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ppt', 'pptx', 'word', 'wordx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template("index.html")

# 拆解filename，获取后缀并判断是否允许上传
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 最关键的代码，调用save函数，传入存储路径作为参数，用os.path.join拼接文件夹和文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
    return render_template("upload.html")

# 获取upload目录下所有文件名
# os.walk函数能获取对应路径下的文件名
def get_filenames(file_dir):
    filenames = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            filenames.append(file)
    return filenames

@app.route('/directory')
def directory():
    # 调用get_filenames获取到upload文件夹下的所有文件名，将文件名传入directory.html中
    # 使用a标签包裹每一个文件名，点击即可下载~
    filenames = get_filenames('upload')
    return render_template("directory.html", filenames=filenames)

@app.route('/download/<filename>')
# 在目录页面下，用户点击对应的a标签，调用download函数，filename作为参数
# 使用send_from_directory方法返回对应目录下的对应文件，直接下载即可
def download(filename):
    return send_from_directory(UPLOAD_PATH, filename, as_attachment=True)

@app.route('/delete/<filename>')
# 在directory.html中就是一个delete的a标签按钮，点击即跳转到delete函数，filename为参数
# delete函数调用os模块中的unlink函数，传入要删除的文件的路径，用os.path.join去拼接路径和文件名
# 返回文件目录页
def delete(filename):
    os.unlink(os.path.join(UPLOAD_PATH, filename))
    return redirect(url_for('directory'))



if __name__ == '__main__':
    app.run()
