from flask import Flask, render_template, request
import os
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def classify_by_color(image_path):
    img = Image.open(image_path).resize((100, 100)).convert('RGB')
    pixels = np.array(img).reshape(-1, 3)
    avg_brightness = np.mean(pixels)

    if avg_brightness < 100:
        return "ขยะรีไซเคิล", "bins/bin_blue.png"
    elif avg_brightness < 140:
        return "ขยะทั่วไป", "bins/bin_red.png"
    elif avg_brightness < 210:
        return "ขยะอินทรีย์", "bins/bin_green.png"
    else:
        return "ขยะอันตราย", "bins/bin_yellow.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    bin_image = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result, bin_image = classify_by_color(filepath)
            print(f"ผลลัพธ์: {result}, รูปถัง: {bin_image}")  # Debug

    return render_template('index.html', result=result, bin_image=bin_image)

if __name__ == '__main__':
    app.run(debug=True)
