# Using Webcam to Detect CNIC image and text show on web browser
In this project use easyocr and cascade classifier to detect text and image respectively.To show detection on web browser use the flask framework. 
In main.py file give the link of all the html files by using render_template firstly index.html file open on browser when run the code. In this page video record of CNIC and save in the 
same file after saving the .avi file and then detect video by click on open recording stop and detection start of video when cascade classifier and easyocr get all value stop detecting the video and show result
on browser.
