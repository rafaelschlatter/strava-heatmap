import os
from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES
from azure.storage.blob import BlockBlobService


def create_app():
    app = Flask(__name__)
    app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
    app.config["photos"] = UploadSet("photos", IMAGES)
    configure_uploads(app, app.config["photos"])

    return app

app = create_app()

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = app.config["photos"].save(request.files["photo"])
        try:
            image = os.path.join(app.config["UPLOADED_PHOTOS_DEST"], filename)
            _upload_to_blob(image=image)
        except Exception as e:
            print("Failed to save image to blob storage.")
            print(e)
        return filename
    return render_template("upload.html")


def _upload_to_blob(image):
    block_blob_service = BlockBlobService(
            account_name=os.environ["STORAGE_ACCOUNT"],
            account_key=os.environ["BLOB_KEY1"],
        )
    blob_name = os.path.basename(image)
    file_path = image
    block_blob_service.create_blob_from_path(
            container_name="imageinput", blob_name=blob_name, file_path=file_path
        )


if __name__ == "__main__":
    app.run()
