import cv2
img=cv2.imread("DATA/00-puppy.jpg")

while True:
    cv2.imshow("Puppy",img)
    if cv2.waitKey(1)& 0xFF==27: #wait 1 ms and press esc key
        break
            
cv2.destroyAllWindows()
