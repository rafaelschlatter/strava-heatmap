import os
from flask import request, render_template, current_app, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from app.upload import upload_bp


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            f = form.file.data
            image = os.path.join(current_app.config["UPLOADED_PHOTOS_DEST"], f.filename)
            form.file.data.save(image)
            _upload_to_blob(
                image=image, block_blob_service=current_app.config["BLOCK_BLOB_SERVICE"]
            )
            flash("Uploaded image successfully to Azure blob storage.", "success")
            return redirect(url_for("upload.upload"))
        except Exception as e:
            flash("Failed to save image to blob storage.", "danger")
            return redirect(url_for("upload.upload"))

    return render_template("upload.html", form=form)


def _upload_to_blob(image, block_blob_service):
    blob_name = os.path.basename(image)
    file_path = image
    block_blob_service.create_blob_from_path(
        container_name="imageinput", blob_name=blob_name, file_path=file_path
    )


class UploadForm(FlaskForm):
    file = FileField(label="Select a file")
    submit = SubmitField(label="Upload image")
