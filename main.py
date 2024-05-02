from flask import Flask, render_template, request
import os
from proccess import get_text
import platform
import db_mgmt
import arrow
import sqlite3

usr_os = platform.system()

app = Flask(__name__)

# Define a list of permitted image file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MEDIA_PATH = "static/images"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



# Define a route for the upload page
@app.route("/upload_image", methods=["GET", "POST"])
def upload_file():
    success = ""
    folder_path = "static/images"

    if request.method == "POST":
        # Check if the POST request has the file part
        if "file" not in request.files:
            return render_template("upload.html", success=False, message="No file part")
        file = request.files["file"]

        # If the user does not select a file, the browser submits an empty part without filename
        if file.filename == "":
            return render_template(
                "upload.html", success=False, message="Please select a file"
            )

        # Check if the file type is allowed
        if file and allowed_file(file.filename):
            # Get the filename entered by the user
            filename = request.form["filename"]

            # Get the extension of the file
            extension = file.filename.split(".")[-1]
            full_filename = os.path.join(folder_path, f"{filename}.{extension}")

            # Check if the filename already exists
            if os.path.exists(full_filename):
                return render_template(
                    "upload.html",
                    success=False,
                    message=f"Filename {filename} "
                    f"already exists, please choose a "
                    f"different name",
                )
            # Use the original filename if no custom name is provided
            if filename == "":
                filename = arrow.now().format("YYYY_MM_DD_HH_MM_SS")
                full_filename = os.path.join(folder_path, f"{filename}.{extension}")
            # Save the uploaded file to a folder with the provided filename
            file.save(full_filename)
            # Add the file path to the database
            db_mgmt.connect_to_db()
            db_mgmt.add_file_path(full_filename, filename)
            return render_template(
                "upload.html", success=True, file_name=f"{full_filename}",
                receipt_name = f"{filename}"
            )
        else:
            return render_template(
                "upload.html", success="False", message="File type not allowed"
            )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET"])
def upload():
    return render_template("upload.html", success="False")


@app.route("/receipt", methods=["GET", "POST"])
def receipt_read():
    receipt_name = request.args.get("receipt_name")
    print(receipt_name)
    db_file_path = db_mgmt.get_path_by_name(receipt_name)[1]
    id = db_mgmt.get_path_by_name(receipt_name)[0]
    print(db_file_path)
    price, date = get_text(str(db_file_path))
    db_mgmt.add_date_and_price(date, price, id)
    return render_template("receipt.html", price=price, date=date)


@app.route("/get_receipt", methods=["GET", "POST"])
def get_receipt():
    rows = db_mgmt.get_table_data()
    return render_template('receipt_table.html', rows=rows)

# @app.route("/show_receipts", methods=["GET", "POST"])
# def show_receipts():



if __name__ == "__main__":
    if usr_os == 'Windows':
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", debug=True)
