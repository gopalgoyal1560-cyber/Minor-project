import streamlit as st
import cv2 
import numpy as np
import classes as tr

#creates title and sub title on streamlit
st.title("Welcome to Your own image filter")
#creates sub heading on streamlit
st.header("Here we provide various types of filter and effects on you images")
#creates 2 radio buttons with a side bar
choice = st.sidebar.radio("Select Image type",["Local image","From Url"])
t = None
if choice == "Local image":
    t = tr.Upload_image() #allow user to load and input image from local storage
elif choice == "From Url":
    if "Image Url" not in st.session_state: #maintains url value permanent until browser session 
        st.session_state["Image Url"] = ""
    st.session_state["Image Url"] = st.text_input("Paste url here",value = st.session_state["Image Url"])
    url = st.session_state["Image Url"]
    if url:
        try: #exeption handling
            t = tr.GetImage(url) #conversion of url content to numpy array for processing is done here
        except Exception as e:
            st.error("Failed to load image")
            t = None

#creats side bar with selectbox to choose effect on image
Effect = st.sidebar.selectbox("Select Process",["Smoothing","Edge Detection","Filter"]) #creates a drop down menu feature

if t is not None and t.img_2 is not None:
    if Effect == "Smoothing":
        smooth = tr.Smoothing()
        method = st.sidebar.selectbox("Smoothing method",["blur","Gaussian blur","Median blur","Bilateral Filter"])
        smooth.Blurring(method,t.img_2) #calls smoothing effects
        tr.Display(t.img_2)
    
    elif Effect == "Edge Detection":
        tr.Edge_detection(t.img_2) #calls edge detection effect
        tr.Display(t.img_2) #display both original and processed image


    #calls filters and dispplay them on image in real time     
    elif Effect == "Filter":
        f = tr.Filter()
        filter_type = st.sidebar.selectbox("Choose Filter",["grayscale","Invert","Brigthness","Hsv"])
        if filter_type == "grayscale":
            f.grayscale(t.img_2)
        elif filter_type == "Invert":
            f.Invert(t.img_2)
        elif filter_type == "Brigthness":
            f.Brigthnes(t.img_2)
        elif filter_type == "Hsv":
            f.Hsv(t.img_2)
        tr.Display(t.img_2)

    tr.Download(t.img_2) #save processed image in predescribed directory after save button is clicked