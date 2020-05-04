from flask import render_template, flash, request, current_app
from flask_mail import Message
from app.contact import contact_bp, mail
from app.forms import ContactForm


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm(request.form)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        if form.validate():
            msg = Message(
                subject="Heatmap feedback from {}".format(name),
                sender=email,
                recipients=[current_app.config["MAIL_USERNAME"]],
            )
            msg.body = message
            mail.send(msg)
            flash("Thank you, {}. Your message has been sent.".format(name))

        else:
            flash("All Fields are Required")

    return render_template("contact.html", form=form)
