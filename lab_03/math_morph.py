import streamlit as st
import numpy as np
import cv2

from utils.utils import uploader, validate_url, FILE_TYPES, get_image, binary
from random import choice
from PIL import Image, ImageChops


CAPTCHA = [
    "https://i.ibb.co/pQ6KPT2/0-wiwh8t-UKBZBZSHiy.jpg"
]

SKELETON = [
    "https://i.ibb.co/ZccJRvp/92607ff7228cdc404d6a2a24aea1c7b9c8fde65e-original.jpg",
    "https://i.ibb.co/8YqpjVD/istockphoto-167634727-612x612.jpg"
]

def dilate(img, k=5, k_size=(3,3)):
    kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, ksize=k_size)
    return cv2.dilate(~img, kernel, iterations=k)


def dilate_2(img, k_size=(3,3)):
    kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, ksize=k_size)
    prev_itr = cv2.dilate(~img, kernel, iterations=1)
    itr = 1
    while True:
        curr_itr = cv2.dilate(~prev_itr, kernel, iterations=1)
        diff = cv2.sumElems(curr_itr)[0] - cv2.sumElems(prev_itr)[0]
        st.write("Curr", cv2.sumElems(curr_itr))
        st.write("Prev", cv2.sumElems(prev_itr))
        st.write(f"This is diff {diff} after {itr} iteration")
        st.write("New approach", cv2.subtract(curr_itr, prev_itr))
        if diff == 0:
            break
        else:
            prev_itr = curr_itr
            itr += 1
    return prev_itr


def dilate_3(img, k_size=(3,3)):
    kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, ksize=k_size)
    prev_itr = cv2.dilate(~img, kernel, iterations=1)
    itr = 1
    while True:
        curr_itr = cv2.dilate(~prev_itr, kernel, iterations=1)
        #im1 = prev_itr.load()
        #im2 = curr_itr.load()
        #result = ImageChops.difference(im1,im2)
        if np.array_equal(prev_itr, curr_itr):
            st.markdown("matches")
            break
        else:
            prev_itr = curr_itr
            itr += 1

    return prev_itr



def erode(img, k=5, k_size=(3,3)):
    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, ksize=k_size)
    return cv2.erode(~img, kernel, iterations=k)


def closing(img, k):
    return dilate(erode(~img, k), k)


def opening(img, k):
    return erode(dilate(~img, k), k)


def condition_dilate(img):
    img = ~img
    elem = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

    minimum = np.minimum(img, cv2.erode(img, elem, iterations=3))
    while True:
        previous = minimum
        minimum = cv2.dilate(minimum, elem)
        result = np.minimum(img, minimum)
        if np.array_equal(result, previous):
            return result
        minimum = result


def skeletoning(img, k_size=(3,3)):
    skeleton = np.zeros(img.shape, np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize=k_size)
    while True:
        erode_img = cv2.erode(img, kernel)
        dilate_img = cv2.dilate(erode_img, kernel)
        subtract = cv2.subtract(img, dilate_img)
        skeleton = cv2.bitwise_or(skeleton, subtract)
        img = erode_img.copy()

        if cv2.countNonZero(img) == 0:
            break
    return skeleton


def description():
    task = '''
    Mathematical morphology:
    
        1. Dilate (extension)
        2. Erode (constriction)
        3. Closing
        4. Opening
        5. Conditional dilate
        6. Skeletoning
        
    Find an image with noisy simple forms, such as a captcha.
    Binarize the image, for example, using the Otsu or Bradley method.
    
    It is better to make a morphological skeleton not on a captcha, but for example on some inscription in a thick font 
    (in huge letters) or, for example, a white horse.
    '''

    st.markdown("### Laboratory work №3")
    st.markdown("**Title:** Mathematical morphology")

    if st.checkbox("Show task"):
        st.write(task)


def show_iters():
    return st.number_input("Number of iterations:", min_value=1, max_value=99, value=2, step=1)


def main():
    description()

    method = st.radio(
        "Choose method:", {
            "1. Dilate (extension)",
            "2. Erode (constriction)",
            "3. Closing",
            "4. Opening",
            "5. Conditional dilate",
            "6. Skeletoning",
        },
        index=5
    )[:1]

    user_img = uploader(st.file_uploader("Upload image:", type=FILE_TYPES))

    user_url = validate_url(
        st.text_input(f"Choose image URL {FILE_TYPES}: ", choice(SKELETON) if method == "6" else choice(CAPTCHA))
    )
    _, gray_image = get_image(user_img, user_url)

    c1, c2 = st.columns(2)

    with c1:
        bin_img = binary(gray_image)
        st.write("Otsu method binarisation:")
        st.image(bin_img, width=300)

    with c2:
        if method == "1":
            k = show_iters()
            #dilate_img = dilate(bin_img, k)
            dilate_img = dilate_3(bin_img)
            st.write("Dilate:")
            st.image(dilate_img, width=300)

        if  method == "2":
            k = show_iters()
            erode_img = erode(bin_img, k)
            st.write("Erode:")
            st.image(erode_img, width=300)

        if method == "3":
            k = show_iters()
            closing_img = closing(bin_img, k)
            st.write("Closing:")
            st.image(closing_img, width=300)

        if method == "4":
            k = show_iters()
            opening_img = opening(bin_img, k)
            st.write("Opening:")
            st.image(opening_img, width=300)

        if method == "5":
            dilate_c_img = condition_dilate(bin_img)
            st.write("Conditional dilate:")
            st.image(dilate_c_img, width=300, clamp=True)

        if method == "6":
            skeletoning_img = skeletoning(bin_img)
            st.write("Morphological skeletoning:")
            st.image(skeletoning_img, width=300)
            st.button("Other image")


if __name__ == "__main__":
    main()