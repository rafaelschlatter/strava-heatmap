import os
from flask import request, render_template, current_app
from app.upload import upload_bp


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = current_app.config["PHOTOS"].save(request.files["photo"])
        try:
            image = os.path.join(current_app.config["UPLOADED_PHOTOS_DEST"], filename)
            _upload_to_blob(image=image, block_blob_service=current_app.config["BLOCK_BLOB_SERVICE"])
            return render_template("upload_success.html")
        except Exception as e:
            print("Failed to save image to blob storage.")
            print(e)
    return render_template("upload.html")


def _upload_to_blob(image, block_blob_service):
    blob_name = os.path.basename(image)
    file_path = image
    block_blob_service.create_blob_from_path(
        container_name="imageinput", blob_name=blob_name, file_path=file_path
    )
