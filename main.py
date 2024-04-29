from flask import Flask, render_template, request
import os
from proccess import get_text
import platform

usr_os = platform.system()

app = Flask(__name__)

# Define a list of permitted image file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MEDIA_PATH = "static/images"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Define a route for the upload page
@app.route("/media", methods=["GET", "POST"])
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
            file_path = os.path.join(folder_path, f"{filename}.{extension}")

            # Check if the filename already exists
            if os.path.exists(file_path):
                return render_template(
                    "upload.html",
                    success=False,
                    message=f"Filename {filename} "
                    f"already exists, please choose a "
                    f"different name",
                )
            # Use the original filename if no custom name is provided
            if filename == "":
                filename = file.filename
            # Save the uploaded file to a folder with the provided filename
            file.save(os.path.join("static/images", f"{filename}.{extension}"))
            return render_template(
                "upload.html", success=True, file_name=f"{filename}.{extension}"
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
    filename = request.args.get("filename")
    print(filename)
    price, date = get_text(f"{MEDIA_PATH}/{filename}")
    return render_template("receipt.html", price=price, date=date)


if __name__ == "__main__":
    if usr_os == 'Windows':
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", debug=True)
