from flask import Flask, render_template, url_for, flash, redirect
from forms import CompInfoForm
from comp_finder import find_comps
import os

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = '6f147f48a92da2c5ce776dc1533259e8'

wca_image = os.path.join(app.config['UPLOAD_FOLDER'], 'wca_logo.png')
loading_gif = os.path.join(app.config['UPLOAD_FOLDER'], 'loading_screen.gif')


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', wca_image=wca_image)


@app.route("/found_comps")
def found_comps_page(states, address):

    competitions = find_comps(states, address)
    CATEGORIES = ['Name', 'URL', 'Date', 'Venue Name', 'Venue Address', 
                            'Distance', 'Reached Competitor Limit']
    comp_strings = [competition.run() for competition in competitions]
    output = [CATEGORIES, comp_strings]

    return render_template('output.html', wca_image=wca_image, output=output, loading_gif=loading_gif)


@app.route("/find_comps", methods=['GET', 'POST'])
def find_comps_page():

    form = CompInfoForm()

    # successfully inputted states and address
    if form.validate_on_submit():

        states = [state.strip() for state in form.states.data.split('\n')]
        address = form.address.data

        return found_comps_page(states, address)

    return render_template('find_comps.html', wca_image=wca_image, form=form, loading_gif=loading_gif)

if __name__ == '__main__':
    app.run(debug=True)
