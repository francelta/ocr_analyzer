from cv2 import VideoCapture
import easyocr
import cv2
import pytesseract
import os
import time

def get_hype(result, img):  
    print("hemos hecho hype")
    
    file =open("info.txt", "a") 
    file.write(str(result[1])+"\n") 
    file.close()
    pt0 = result[0][0][0]
    
    cv2.circle(img, pt0, 1, (0, 0, 255), -1)
    
    pt1 = result[0][0][1]
    cv2.circle(img, pt1, 1, (0, 0, 255), -1)
    pt2 = result[len(result)-1][0][2]
    cv2.circle(img, pt2, 1, (0, 0, 255), -1)
    pt3 = result[len(result)-1][0][3]
    cv2.circle(img, pt3, 1, (0, 0, 255), -1)
   
    ptx=int((pt1[0]-pt0[0])//30)+pt0[0]
    cv2.circle(img, (ptx,pt0[1]), 1, (0, 0, 255), -1)
    cv2.circle(img, result[0][0][3], 1, (0, 0, 255), -1)
    ptg=result[0][0][3]
    ptmedida= ptx+(ptx-pt0[0])
    ptz=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    ptz[0]=ptx
    for i in range(1,30):
        ptz[i]=ptx+(ptx-pt0[0])*i  
        cv2.circle(img, (ptz[i],pt0[1]), 1, (0, 0, 255), -1)
    
    
    
    
    
    # cv2.rectangle(img, pt0[0:640], (pt1[0], pt1[1] - 23), (255,0,0),-1)
    # cv2.putText(img, res[1], (pt0[0], pt0[1] -3),2, 0.8, (255,255,255),1)
    # cv2.rectangle(img, pt0, pt2, (255,0,0),2)
    cv2.imshow("Image", img)
    print("hemos pillao texto")
    k = cv2.waitKey (0) # waitkey significa leer la entrada del teclado, y el número entre paréntesis indica cuánto tiempo esperar en ms 0 significa esperar
    if k == 27: # Valor clave de la tecla Esc en el teclado
        cv2.destroyAllWindows() 

def croper(cropfile, img, medida):
    cropfile = img[medida]
    result = reader.readtext(cropfile)
    get_hype(result, cropfile)


def imageMaker():
    cap=VideoCapture(0)
    borde=100
    ancho=640
    alto =480
    cap.set(3, ancho) #DEFINIMOS EL WIDTH // CON EL PRIMER PARÁMERTRO IDENTIFICAMOS EL ID DE WIDTH
    cap.set(4, alto) #DEFINIMOS EL HEIGTH // CON EL PRIMER PARÁMERTRO IDENTIFICAMOS EL ID DE HEIGHT
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            window_name = 'frame'
            font = cv2.FONT_ITALIC
            org = (borde, int(borde*0.8))
  
            # fontScale
            fontScale = 0.8
            # Blue color in BGR
            color = (255, 10, 10)
            thickness = 1
            # Using cv2.putText() method
            image = cv2.putText(frame, 'coloque su documento en el recuadro', org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
            start_point = (int(borde), int(borde*1.15))
            end_point = (int(ancho-borde), alto-int(borde*1.15))
            
            cv2.rectangle(frame, start_point, end_point, color, thickness)
            cv2.imshow('frame', frame)
            # Si se pulsa una tecla guardamos su valor en 'key'
            key = cv2.waitKey(1)
            if key == 27:#escape
                break
            elif key == 32:
                # Si queremos guardar frame actual apretamos tecla 'espacio' (ascii=32)
                print('Hacemos foto')
                frame = frame[borde:alto-borde, borde:ancho-borde]#es al revés de como hacemos siempre
                cv2.imwrite('img.png', frame)
                cv2.destroyAllWindows()
                break
        else:
            break
    return(0)    
file=open('info.txt', 'w')
file.close()
#imageMaker()        
reader = easyocr.Reader(["es", "en"], gpu=False)
#image=cv2.imread('img.png')
image=cv2.imread('imagen_matricula.jpeg')
cv2.imshow('Image', image)
print("sale una foto")
height, width, channels = image.shape
print(height,width)


print("sale otra foto")
file =open("info.txt", "r") 
tipe=file.readlines()


crop_img3 =image[int(height*0.68): int(height), 0: width]
print("y otra")
resultar = reader.readtext(crop_img3)
print(resultar)
get_hype(resultar, crop_img3)
print("la última")
cv2.waitKey(0)
fecha = time.strftime("%Y%m%d-%H%M%S")
print(fecha)
dst = './dataprocesado/'+fecha+'.png'
print(dst)
os.rename('img.png', dst)
dst2 = './dataprocesado/'+fecha+'.txt'
os.rename('info.txt', dst2)
cv2.destroyAllWindows()

