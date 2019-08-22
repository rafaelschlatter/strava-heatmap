import os
from flask import render_template, current_app
from azure.storage.blob import BlockBlobService
from app.process import process_bp


@process_bp.route("/process")
def process():
    block_blob_service = BlockBlobService(
        account_name=os.environ["STORAGE_ACCOUNT"], account_key=os.environ["BLOB_KEY1"]
    )
    block_blob_service.get_blob_to_path(
        container_name="imageinput",
        blob_name="test_separator.png",
        file_path=os.path.join(current_app.config["TEMP_DIR"], "test_separator.png"),
    )

    return render_template("base.html")


def _list_images():
    block_blob_service = BlockBlobService(
        account_name=os.environ["STORAGE_ACCOUNT"], account_key=os.environ["BLOB_KEY1"]
    )
    blob_generator = block_blob_service.list_blobs(container_name="imageinput")
