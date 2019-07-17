from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class CompInfoForm(FlaskForm):
    """Input Form to get info about what comps to find, 
       and what info to get about the comps"""

    # textarea for inputting states to find competitions in
    states = TextAreaField(
            'States', 
            validators=[
                DataRequired(), 
                Length(min=4, max=471)
                ],
            render_kw={
                'rows': '10', 
                'cols': '77'
                }
            )

    # checkboxes for information types
    date = BooleanField(
        'Date',
        render_kw={'class': 'checkbox'}
    )
    venue = BooleanField(
        'Venue',
        render_kw={'class': 'checkbox'}
    )
    website_link = BooleanField(
        'Website Link',
        render_kw={'class': 'checkbox'}
    )
    venue_address = BooleanField(
        'Venue Address',
        render_kw={'class': 'checkbox'}
    )
    driving_distance = BooleanField(
        'Driving Distance',
        render_kw={'class': 'checkbox'}
    )
    reached_competitor_limit = BooleanField(
        'Reached Competitor Limit',
        render_kw={'class': 'checkbox'}
    )

    submit = SubmitField('Find Competitions Near You', render_kw={'onclick': 'showDiv()'})


class AddressForm(FlaskForm):
    """address to know distance to competitions for"""
    address = StringField(
        'Address or Coordinates:', 
        validators=[DataRequired()],
        render_kw={'size': '79'}
        )

    submit = SubmitField('Submit Address', render_kw={'onclick': 'showDiv()'})
