import cv2
import numpy as np
import streamlit as st
import requests
import io

class Upload_image:
    def __init__(self):
        self.img_2 = None
        
        # Allow user to select image of given types from local storage
        file = st.file_uploader("Select image from here",type = ["jpeg","png","jpg"])
        if file is not None:
            file_bytes = np.frombuffer(file.read(),np.uint8) #adjust bytes to take image as numpy array 
            img = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR) # Read image in BGR Color
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #convert BGR to RGB
            self.img_2 = img.copy() #copies real image so we can see results by comparing side by side
            if "Image" not in st.session_state:
                st.session_state["Image"] = img.copy() #maintains image values stable so image do not get refreshed in streamlit each user interation

    
class Smoothing:
    def Blurring(self,filter,img):
        if "Image" in st.session_state:
            if filter == "blur":
                st.session_state["Image"] = cv2.blur(img, (35,35)) #calls predefined blur functions from opencv Library to appply on image
            if filter == "Gaussian blur":
                st.session_state["Image"] = cv2.GaussianBlur(img, (25,25), 0)#calls Gaussian blur to apply on image
            if filter == "Median blur":
                st.session_state["Image"] = cv2.medianBlur(img,11) #calls Median blur to apply on image
            if filter == "Bilateral Filter":
                st.session_state["Image"] = cv2.bilateralFilter(img,15,100,100) #calls bilateral filter to apply on image
        
class Edge_detection:
    def __init__(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #convert RGB image to gray to do edge detection
        edge = cv2.Canny(gray,50,100) #edge detection function from opencv
        edge = cv2.cvtColor(edge,cv2.COLOR_GRAY2RGB) #reconvert Gray to RGB
        st.session_state["Image"] = edge #stores changes
        

class Filter:
    def grayscale(self,img):
        st.session_state["Image"] = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #takes RGB channels and adjust color intensity to make image gray
    
    def Invert(self,img):
        st.session_state["Image"] = cv2.bitwise_not(img) #convert dark pixels bright adn bright to dark
    
    def Brigthnes(self,img):
        brightness = st.sidebar.slider("Brightness",-100,100,0) #introduce a slidebar in streamplit 
        img_64 = img.astype(np.int64)
        img_64 = img_64 + brightness #increase intensity of each pixel while keeping color format same
        st.session_state["Image"] = np.clip(img_64,0,255).astype(np.uint8) #cap to range of pixel values to stable output

    def Hsv(self,img):
        st.session_state["Image"] = cv2.cvtColor(img,cv2.COLOR_RGB2HSV) #convert image to hsv



class Display:
    def __init__(self,og_img):
        col1,col2 = st.columns(2)
        with col1:
            st.image(og_img,caption = "Original") #diplay original image to see result by comparing processed image
        with col2:
            st.image(st.session_state["Image"],caption = "Processed") #show processed image

class Download:
    def __init__(self,image):
        if st.button("Final"): #creates a button on streamlit
            image = st.session_state["Image"] 
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)#converts image back to BGR to save 
            success,encoded_img = cv2.imencode(".png",image)
            if success:
                st.success("Image processing is comepleted") #Signal successful conversion of image in png format
                img = encoded_img.tobytes()
                st.download_button(
                label="Download Image",
                data=img,
                file_name="processed.png",
                mime="image/png"
            )
            else:
                st.error("Image encoding failed")

class GetImage:
    def __init__(self,url):
        self.img_2 = None
        response = requests.get(url)
        img_byte = np.asarray(bytearray(response.content),dtype = np.uint8)
        img = cv2.imdecode(img_byte,cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.img_2 = img.copy()
        if "Image" not in st.session_state:
            st.session_state["Image"] = img.copy()



