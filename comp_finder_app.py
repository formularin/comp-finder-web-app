from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from forms import CompInfoForm
from comp_finder import find_comps
import os
import time

CWD = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = '6f147f48a92da2c5ce776dc1533259e8'

Bootstrap(app)

wca_image = os.path.join(app.config['UPLOAD_FOLDER'], 'wca_logo.png')
loading_gif = os.path.join(app.config['UPLOAD_FOLDER'], 'loading_screen.gif')

with open(f'{CWD}/states.txt', 'r') as f:
    ALL_STATES = [state.strip() for state in f.read().split('\n')]

# create webdriver without physical window
op = ChromeOptions()
op.add_argument('headless')
driver = Chrome(f'{CWD}/chromedriver', options=op)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', wca_image=wca_image)


@app.route("/invalid")
def invalid_page(**kwargs):
    return render_template('invalid.html', wca_image=wca_image, **kwargs)


@app.route("/found_comps")
def found_comps_page(information_types, states, address):

    output = find_comps(states, address, information_types)

    return render_template('output.html', wca_image=wca_image, output=output, loading_gif=loading_gif)


@app.route("/find_comps", methods=['GET', 'POST'])
def find_comps_page():

    form = CompInfoForm()

    # successfully inputted states and address
    if form.validate_on_submit():

        # get data from inputs
        states = [state.strip() for state in form.states.data.split('\n')]
        address = form.address.data
        
        # catch all states that aren't in list of states
        invalid_states = []
        for state in states:
            if state not in ALL_STATES:
                invalid_states.append(state)

        states_are_valid = bool(invalid_states == [])
        
        # search for location on google maps
        driver.get('https://www.google.com/maps')
        time.sleep(2)
        input_field = driver.find_element_by_class_name('tactile-searchbox-input')
        input_field.send_keys(address)
        input_field.send_keys(Keys.ENTER)

        time.sleep(2)

        address_is_valid = bool(len(driver.find_elements_by_class_name('section-bad-query-title')) == 0)

        if not address_is_valid and not states_are_valid:
            return invalid_page(invalid=['states', 'address'], states=invalid_states, address=address)
        elif not address_is_valid and states_are_valid:
            return invalid_page(invalid=['address'], address=address)
        elif address_is_valid and not states_are_valid:
            return invalid_page(invalid=['states'], states=invalid_states)

        information_types = []

        if form.date.data:
            information_types.append('date')
        if form.venue.data:
            information_types.append('venue')
        if form.website_link.data:
            information_types.append('website_link')
        if form.venue_address.data:
            information_types.append('venue_address')
        if form.driving_distance.data:
            information_types.append('driving_distance')
        if form.reached_competitor_limit.data:
            information_types.append('reached_competitor_limit')

        return found_comps_page(information_types, states, address)

    return render_template('find_comps.html', wca_image=wca_image, form=form, loading_gif=loading_gif)

# temporary test for output table styling
@app.route("/test-output")
def test_output_page():
    return render_template('test_output.html', wca_image=wca_image)

if __name__ == '__main__':
    app.run(debug=True)
