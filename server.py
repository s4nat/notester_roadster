from flask import Flask, jsonify, request
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import base64
from PIL import Image
import io
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

img_list = []

@app.route('/notesupload', methods=['POST'])
def post_notes():
    uri = request.get_json()
    b64 = uri['uri']
    img_list.append(uri)


    encoded_data = b64.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    rv = []

    for b in boxes.splitlines():
        b = b.split(' ')
        # (a, b) a = top right xy coordinates, b = bottom right xy coordinate * ratio form
        rv.append(((int(b[1]) / w, (h - int(b[2])) / h), (int(b[3]) / w, (h - int(b[4])) / h)))

    return jsonify({"rv": rv})

app.run()
