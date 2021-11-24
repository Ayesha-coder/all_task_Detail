from logging import debug
import cv2
from flask import Flask, render_template, request, Response
import easyocr
from easyocr import Reader
import face_detect_camera
import os

camera_on_off = True
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def generate_frames():
    camera= cv2.VideoCapture(0)
    fourcc=cv2.VideoWriter_fourcc(*'XVID')

    out=cv2.VideoWriter('output2.avi',fourcc,20.0,(640,480))

    while camera_on_off:
        ## read the camera frame

        success,frame=camera.read()
        if not success:
            break

        out.write(frame)
        cv2.waitKey(41)
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            

        yield(b'--frame\r\n'

                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    out.release()



filePath = 'output2.avi'

if os.path.exists(filePath):
    os.remove(filePath)

filePath = 'static/detect_face.jpg'

if os.path.exists(filePath):
    os.remove(filePath)

@app.route("/second")
def second():
    return render_template("camera.html")

@app.route("/result")
def result():
    global camera_on_off
    camera_on_off = False
    return render_template("result.html", context=face_detect_camera.final_result())

# @app.route("/detect")
# def detect():
#     return Response(detect_image())

@app.route("/video")
def video():
    return Response(generate_frames(),
    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":  
    app.run(debug=True)

