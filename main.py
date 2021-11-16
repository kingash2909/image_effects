import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation = request.form['image']
    print(operation)
    file = request.files['file']
    filename = secure_filename(file.filename)
    in_stream = file.read()
    arr = np.fromstring(in_stream, dtype='uint8')

    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    if operation == 'oil':
        file_data = oil_effect(img)
    elif operation == 'water':
        file_data = water_color_effect(img)
    elif operation == 'sketch':
        file_data = image_sketch(img)
    else:
        file_data = rgb_effect(img)

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)


def image_sketch(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert_img = cv2.bitwise_not(gray)
    blur_img = cv2.GaussianBlur(invert_img, (111, 111), 0)
    invblur_img = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(gray, invblur_img, scale=256.0)

    not_needed, out_stream = cv2.imencode('.PNG', sketch_img)

    return out_stream

def oil_effect(img):

    res = cv2.xphoto.oilPainting(img, 7, 1)

    not_needed, out_stream = cv2.imencode('.PNG', res)

    return out_stream

def water_color_effect(img):
    res = cv2.stylization(img, sigma_s=60, sigma_r=0.6)

    not_needed, out_stream = cv2.imencode('.PNG', res)

    return out_stream

def rgb_effect(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


    not_needed, out_stream = cv2.imencode('.PNG', rgb)

    return out_stream


@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()
