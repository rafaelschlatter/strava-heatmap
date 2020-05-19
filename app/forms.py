from wtforms import Form, StringField
from flask_wtf import RecaptchaField
from wtforms.validators import InputRequired, Email


class ContactForm(Form):
    name = StringField("Name", validators=[InputRequired("Please enter your name.")])
    email = StringField("Email", validators=[
        InputRequired("Please enter your email address."),
        Email("Please enter a valid email address.")]
    )
    message = StringField("Message", validators=[InputRequired("Please enter a message.")])
    recaptcha = RecaptchaField("ReCaptcha")
