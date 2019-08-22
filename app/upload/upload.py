import os
from flask import request, render_template, current_app, flash, redirect, url_for
from app.upload import upload_bp


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        try:
            filename = current_app.config["PHOTOS"].save(request.files["photo"])
            image = os.path.join(current_app.config["UPLOADED_PHOTOS_DEST"], filename)
            _upload_to_blob(
                image=image, block_blob_service=current_app.config["BLOCK_BLOB_SERVICE"]
            )
            flash("Uploaded image successfully to Azure blob storage.", "success")
            return redirect(url_for("upload.upload"))
        except Exception as e:
            flash("Failed to save image to blob storage.", "danger")
            return redirect(url_for("upload.upload"))

    return render_template("upload.html")


def _upload_to_blob(image, block_blob_service):
    blob_name = os.path.basename(image)
    file_path = image
    block_blob_service.create_blob_from_path(
        container_name="imageinput", blob_name=blob_name, file_path=file_path
    )
