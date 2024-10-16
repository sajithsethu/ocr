import os
from flask import Flask, request, render_template
from PIL import Image
import pytesseract

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads and OCR
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part in request", 400
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Perform OCR on the saved image
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        return render_template('index.html', ocr_text=text, image_path=filepath)

# Start the app
if __name__ == '__main__':
    app.run(debug=True)

