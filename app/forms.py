from wtforms import Form, StringField
from wtforms.validators import InputRequired


class ContactForm(Form):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    message = StringField("Message", validators=[InputRequired()])
