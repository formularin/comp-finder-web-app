from flask import Flask, render_template
import os

LOGO_FOLDER = os.path.join('static', 'logos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = LOGO_FOLDER

wca_image = os.path.join(app.config['UPLOAD_FOLDER'], 'wca_logo.png')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', wca_image=wca_image)

@app.route("/find_comps")
def find_comps():
    return render_template('find_comps.html', wca_image=wca_image)

if __name__ == '__main__':
    app.run(debug=True)
