import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cascade = cv2.CascadeClassifier('C:\Python311\Lib\site-packages\cv2\data\haarcascade_russian_plate_number.xml')
states = {"AN":"Andaman and nicobar","AP":"Andhra pradesh","AR":"Arunachal pradesh","AS":"Assam","BR":"Bihar",
          "CH":"Chandigarh","DN":"Dadra and Nagar Haveli","DD":"Daman and Diu","DL":"Delhi","GA":"Goa","GJ":"Gujarat",
          "HR":"Haryana","HP":"Himachal pradesh","JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala","LD":"Lakshadweep",
          "MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland",
          "OR":"Orissa","PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"Tamil Nadu","TR":"Tripura",
          "UP":"Uttar Pradesh","WB":"West Bengal"}
def extract_num(img_name):
    global read
    img = cv2.imread(img_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate = cascade.detectMultiScale(gray,1.1,4)

    for (x, y, w, h) in nplate:
        a,b=(int(0.02*img.shape[0]),int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b,:]

        kernel=np.ones((1,1),np.uint8)
        plate = cv2.dilate(plate,kernel,iterations=1)
        plate = cv2.erode(plate,kernel,iterations=1)
        plate_gray=cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)

        read=pytesseract.image_to_string(plate)
        print(read)
        read=''.join(e for e in read if e.isalnum())
        stat=read[0:2]
        try:
            print('car belongs to ',states[stat])
        except:
             print('state not recognized')
        print(read)

        cv2.rectangle(img,(x, y), (x + w, y + h), (51,51,255), 2)
        cv2.rectangle(img,(x,y-40),(x+w,y),(51,51,255),-1)
        cv2.putText(img, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Plate',plate)


    cv2.imshow('Result',img)
    cv2.imwrite('result.jpeg',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

extract_num(r"C:\Users\rashmi\Downloads\WhatsApp Image 2023-08-29 at 3.20.05 PM.jpeg")

