from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


class ContactForm(Form):
    name = TextField("Name", validators=[validators.required()])
    email = TextField("Email", validators=[validators.required()])
    message = TextField("Message", validators=[validators.required()])
