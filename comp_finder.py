from flask import Flask, render_template, url_for, flash, redirect
from forms import InputFileForm
import os

LOGO_FOLDER = os.path.join('static', 'logos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = LOGO_FOLDER
app.config['SECRET_KEY'] = '6f147f48a92da2c5ce776dc1533259e8'

wca_image = os.path.join(app.config['UPLOAD_FOLDER'], 'wca_logo.png')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', wca_image=wca_image)

@app.route("/find_comps", methods=['GET', 'POST'])
def find_comps():
    form = InputFileForm()
    if form.validate_on_submit():
        flash('states and address successfully submitted', 'success')
        return redirect(url_for(home))
    return render_template('find_comps.html', wca_image=wca_image, form=form)

if __name__ == '__main__':
    app.run(debug=True)
