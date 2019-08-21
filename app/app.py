import os
from flask import Flask, request, render_template
from flask_uploads import configure_uploads
from flask_bootstrap import Bootstrap
from azure.storage.blob import BlockBlobService
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_uploads(app, app.config["PHOTOS"])
    bootstrap = Bootstrap(app)

    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = app.config["PHOTOS"].save(request.files["photo"])
        try:
            image = os.path.join(app.config["UPLOADED_PHOTOS_DEST"], filename)
            _upload_to_blob(image=image)
            
        except Exception as e:
            print("Failed to save image to blob storage.")
            print(e)

        return filename
    return render_template("upload.html")


@app.route("/process")
def process():
    block_blob_service = BlockBlobService(
            account_name=os.environ["STORAGE_ACCOUNT"],
            account_key=os.environ["BLOB_KEY1"],
        )
    block_blob_service.get_blob_to_path(container_name="imageinput", blob_name="test_separator.png", file_path=os.path.join(app.config["TEMP_DIR"], "test_separator.png"))

    
    return render_template("base.html")


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

def _list_images():
    block_blob_service = BlockBlobService(
            account_name=os.environ["STORAGE_ACCOUNT"],
            account_key=os.environ["BLOB_KEY1"],
        )
    blob_generator = block_blob_service.list_blobs(container_name="imageinput")


if __name__ == "__main__":
    app.run()
