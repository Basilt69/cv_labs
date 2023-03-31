import streamlit as st
import numpy as np
import cv2

from utils.utils import validate_url, uploader, get_image, FILE_TYPES
from PIL import Image

URL = "https://yandex.ru/images/search?from=tabbar&img_url=http%3A%2F%2Fnationalvanguard.org%2Fwp-content%2Fuploads%2F20" \
      "17%2F09%2FLL-Blog_Sorens_Kantian-Liberalism_1200-1024x576.jpg&lr=213&pos=12&rpt=simage&text=Kant"


def show_cols():
    # input of parameters for OpenCV.GaussianBlur
    c1, c2 = st.columns()
    with c1:
        dim = st.number_input("Kernel size:", min_value=1, max_value=99, value=3, step=2)
    with c2:
        sig = st.number_input("Sigma:", min_value=1, max_value=99, value=3, step=2)

    return c1, c2, dim, sig


def main():
    st.markdown("## Laboratory work №1")
    st.markdown("### **Title**: Gaussian blur")
    st.markdown("---")

    st.markdown("""In image processing, a Gaussian blur (also known as Gaussian smoothing) is the result of blurring an
    image by a Gaussian function (named after mathematician and scientist Carl Friedrich Gauss).It is a widely used 
    effect in graphics software, typically to reduce image noise and reduce detail. The visual effect of this blurring 
    technique is a smooth blur resembling that of viewing the image through a translucent screen, distinctly different 
    from the bokeh effect produced by an out-of-focus lens or the shadow of an object under usual illumination. 
    Gaussian smoothing is also used as a pre-processing stage in computer vision algorithms in order to enhance image
    structures at different scales—see scale space representation and scale space implementation.""")
    st.markdown("---")

    user_img = uploader(st.file_uploader("Upload your image:", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Insert url of your image {FILE_TYPES}: ", URL))

    _, gray_image = get_image(user_img, user_url)

    func = st.radio(
        "Choose your filter:", (
            "1. OpenCV GaussianBlur",
            "2. Step by step implementation",
        ),
        index=0
    )

    if func[:1] == "1":
        c1, c2,dimension, sigma = show_cols()

        res = cv2.GaussianBlur(gray_image, (dimension, dimension), sigma)

        with c2:
            st.image(res, width=300)





if __name__ == "__main__":
    main()

