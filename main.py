from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from colorthief import ColorThief
from werkzeug.utils import secure_filename

FOLDER = UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FOLDER
app.config["SECRET_KEY"] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class UploadForm(FlaskForm):
    file = FileField()


@app.route("/", methods=["POST", "GET"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(app.config['UPLOAD_FOLDER'] + filename)
        return image(filename)
    return render_template("index.html", form=form)


@app.route("/image", methods=["POST", "GET"])
def image(filename):
    path = app.config['UPLOAD_FOLDER'] + filename
    color_thief = ColorThief(path)
    palette = color_thief.get_palette(color_count=8)
    return render_template("image.html", pallete=palette, path=path)


if __name__ == '__main__':
    app.run(debug=True)
