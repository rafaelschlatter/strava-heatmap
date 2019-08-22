import os
from flask import render_template, current_app
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
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

    blob_names = _list_images()
    form = ProcessForm()
    form.selection.choices = [(index, name) for index, name in enumerate(blob_names)]
    return render_template("process_form.html", form=form)


def _list_images():
    block_blob_service = BlockBlobService(
        account_name=os.environ["STORAGE_ACCOUNT"], account_key=os.environ["BLOB_KEY1"]
    )
    blob_generator = block_blob_service.list_blobs(container_name="imageinput")
    blob_names = []
    for blob in blob_generator:
        blob_names.append(blob.name)

    return blob_names


class ProcessForm(FlaskForm):
    selection = SelectField(u"Select image", coerce=int)
    submit = SubmitField("Process image")
