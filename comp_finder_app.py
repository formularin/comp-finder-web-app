from flask import Flask, render_template, url_for, flash, redirect
from forms import InputFileForm
from comp_finder import find_comps
import os

LOGO_FOLDER = os.path.join('static', 'logos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = LOGO_FOLDER
app.config['SECRET_KEY'] = '6f147f48a92da2c5ce776dc1533259e8'

wca_image = os.path.join(app.config['UPLOAD_FOLDER'], 'wca_logo.png')

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', wca_image=wca_image)

@app.route("/find_comps", methods=['GET', 'POST'])
def find_comps_page():
    form = InputFileForm()
    # successfully inputted states and address
    if form.validate_on_submit():
        states = form.states.data.split('\n')
        address = form.address.data
        competitions = find_comps(states, address)
        categories = ['Name', 'URL', 'Date', 'Venue Name', 'Venue Address', 
                                    'Distance', 'Reached Competitor Limit']
        output = [categories, [competition.run() for competition in competitions]]
        return render_template('output.html', output=output)
    return render_template('find_comps.html', wca_image=wca_image, form=form)

if __name__ == '__main__':
    app.run(debug=True)
