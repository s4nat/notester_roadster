from flask import Flask, jsonify, request
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import base64
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# @app.route("/notesteroadster")
# def readb64(uri):
#    encoded_data = uri.split(',')[1]
#    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
#    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    return img
#
# # img = readb64(data_uri)
# # print(img)
# # img = cv2.imread("tester.jpg")
#
#
#
# text = pytesseract.image_to_string(img)
# sentences = []
# line = ""
# for i in text:
#     if i != ".":
#         if i != "\n":
#             if line == "" and not(i.isalpha()):
#                 continue
#             else:
#                 line += i
#         else:
#             line += " "
#     else:
#         line += "."
#         sentences.append(line.lstrip())
#         line = ""
#
# for i in sentences:
#     print(i)
#
# app.run()

img_list = []

@app.route('/notesupload', methods=['POST'])
def post_notes():
    uri = request.get_json()
    img = uri['uri']
    img_list.append(uri)
    return jsonify(img)


@app.route('/notesupload')
def get_sentences():
    for img in img_list:
        uri = img['uri']
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    text = pytesseract.image_to_string(img)
    sentences = []
    line = ""
    for i in text:
       if i != ".":
           if i != "\n":
               if line == "" and not(i.isalpha()):
                   continue
               else:
                   line += i
           else:
               line += " "
       else:
           line += "."
           sentences.append(line.lstrip())
           line = ""

    # text = pytesseract.image_to_data(img, output_type=Output.DICT)
    # print(text.keys())
    #
    # return jsonify({'sentences': sentences})

app.run()