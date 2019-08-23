import os
from flask import render_template, current_app, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app.process import process_bp


@process_bp.route("/process", methods=["GET", "POST"])
def process():
    blob_names = _list_images(
        block_blob_service=current_app.config["BLOCK_BLOB_SERVICE"]
    )
    form = ProcessForm()
    choices = [(index, name) for index, name in enumerate(blob_names)]
    if len(choices) == 0 or choices == None:
        flash(
            "No images uploaded yet. You need to upload an image before you can process it.",
            "danger",
        )
    form.selection.choices = choices

    if form.validate_on_submit():
        image = dict(form.selection.choices).get(form.selection.data)
        filepath = os.path.join(current_app.config["TEMP_DIR"], str(image))
        current_app.config["BLOCK_BLOB_SERVICE"].get_blob_to_path(
            container_name="imageinput", blob_name=str(image), file_path=filepath
        )

        image_for_processing = filepath
        # Here needs to come the call to run() method from the algorithm class engineering-drawing-cv
        # The image above

        flash("Image processed successfully.", "success")
        return redirect(url_for("process.process"))

    return render_template("process.html", form=form)


def _list_images(block_blob_service):
    blob_generator = block_blob_service.list_blobs(container_name="imageinput")
    blob_names = []
    for blob in blob_generator:
        blob_names.append(blob.name)

    return blob_names


class ProcessForm(FlaskForm):
    selection = SelectField(u"Select image", coerce=int)
    submit = SubmitField("Process image")
