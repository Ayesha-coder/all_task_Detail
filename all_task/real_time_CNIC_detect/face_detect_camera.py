import easyocr
import os
import cv2


def final_result():
    data_dict={}
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def detect_from_video(video_path):
        camera= cv2.VideoCapture(video_path)
        detect_image(camera)
        return get_data(camera)

    def detect_image(camera):  

            while True:
            ## read the camera frame

                success,frame=camera.read()
                if not success:
                    break
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces, detection = faceCascade.detectMultiScale2(grayscale, 1.3, 5)
                # print('faces', faces)
                # print('detection', detection)
                for (x, y, w, h) in faces:
                    # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    frame = frame[y-40:y+h+40, x-40:x+w+40]
                if detection and detection[0]>30:
                    if cv2.imwrite('static/detect_face.jpg', frame) == True:
                        break


    def get_data(camera):
        get = easyocr.Reader(['en'])
        Name=Father_Name=Gender=Id_Number=D_O_Birth=D_O_Issue=D_O_Expiry='-'
        data_dic={
                'Name' : '-',
                'Gender' : '-', 
                'Identity Number' : '-', 
                'Date Of Birth' : '-', 
                'Date Of Issue' : '-', 
                'Date Of Expiry' : '-'}
            
        while True:

            success,frame=camera.read()
            if not success:
                break
            data = get.readtext(frame)
            lis=[]
            for i in range(0,len(data)):
                lis.append(data[i][1])
            data=lis

            gaurdian='Father Name'
            #father name
            if list(filter(lambda x: 'Father' in x, data)) and Father_Name=='-':
                Father_Name=data[data.index(list(filter(lambda x: 'Father' in x, data))[0])+1]
            elif list(filter(lambda x: 'Husband' in x, data)) and Father_Name=='-':
                Father_Name=data[data.index((list(filter(lambda x: 'Husband' in x, data)))[0])+1]
                gaurdian="Husband Name"
                Gender='F'
            #name
            if "Name" in data and Name=='-':
                Name=data[data.index("Name")+1]
            if Name == "-":
                _name=list(filter(lambda x: 'Nam' in x, data))
                if _name and not bool(list(filter(lambda x: 'Father' in x, _name))):
                    Name=data[data.index(list(filter(lambda x: 'Nam' in x, data))[0])+1]
                elif Father_Name != "-":
                    Name=data[data.index(list(filter(lambda x: 'Father' in x, data))[0])-1]


            #gender
            if "F" in data and Gender=='-':
                Gender='F'
            elif "M" in data and Gender=='-':
                Gender='M'
            #id_number
            if list(filter(lambda x: x.count('-')==2, data)) and Id_Number=='-':
                Id_Number=list(filter(lambda x: '-' in x, data))[0]
            #dates
            if len(list(filter(lambda x: '.' in x, data)))==3:
                D_O_Birth,D_O_Issue,D_O_Expiry=list(filter(lambda x: '.' in x, data))
            #assign data
            data_dic={
                'Name':Name,
                gaurdian:Father_Name,
                'Gender':Gender, 
                'Identity Number':Id_Number, 
                'Date Of Birth':D_O_Birth, 
                'Date Of Issue':D_O_Issue, 
                'Date Of Expiry':D_O_Expiry}
            
            if '-' not in data_dic.values():
                break
        return data_dic
    
    return detect_from_video('output2.avi') 
    


