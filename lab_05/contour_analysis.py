import cv2
import streamlit as st
import numpy as np

from utils.utils import loader

PATTERN_URL = "https://img.favpng.com/18/12/25/triangle-blue-shape-png-favpng-GiyVGMhuhVfrT688Zw5x4DGXH.jpg"
URL = "https://rus-linux.net/images/soft/pgf/Figure-2-Three-colored-triangles-with-PGFTikZ.png"
COLOR = (0, 255, 0)


def description():

    task = """
    - VC - vector-contour
    - NSP - normalized scalar product
    - MCF - mutual correlation function
    - AFVC - autocorrelation function of VC
    
    Algorithm:
    1. Image preprocessing (anti-aliasing, noise filtering, contrast enhancement)
    2. Selection of object boundaries (preferably using Canny)
    3. Preliminary filtering of boundaries by size and other features (perimeter, area, etc.)
    4. Coding of closed borders without self-intersections in the form of VC
    5. Reduction of VC to a single length, smoothing (equalization of VC)
    6. Comparison of all found VC with the reference VC using the "tau max module"
    
    To realize:
    - in paint, sketch geometric shapes, such as a triangle
    - encode such a triangle and find it on a random image
    - the program should find the shapes
    """

    st.markdown("### Laboratory work №5")
    st.markdown("**Title:** Contour analysis")

    if st.checkbox("Show task"):
        st.write(task)
    st.markdown("---")


def get_contours(gray, color):
    c1, c2 = st.colomns(2)
    if c1.checkbox("Blur", value=True):
        gray = cv2.GaussianBlur(gray, (3,3), cv2.BORDER_DEFAULT)

    if c2.checkbox("Detect boundaries", value=True):
        gray = cv2.Canny(gray, 50, 150)

    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    c1.image(thresh)

    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    image_copy = np.uint8(color).copy()
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=COLOR, thickness=2, lineType=cv2.LINE_AA)
    c2.image(image_copy)


def match_by_template(c_img, img, pattern, threshold=0.8):
    w, h = pattern.shape[::-1]

    res = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(c_img, pt, (pt[0] + w, pt[1] + h), COLOR, 2)

    st.image(c_img)


def main():
    description()

    c_patter, gray_pattern = loader(PATTERN_URL, txt="pattern")
    color_img, gray_img = loader(URL, txt="image")

    h, w = gray_img.shape[:2]

    st.markdown("---")

    found = []
    t_h, t_w = gray_pattern.shape[:2]
    template_edged = cv2.Canny(gray_pattern, 50, 200)

    st.write("template_edged:")
    st.image(template_edged)

    i = 0
    for scale in np.linespace(1, 2, 20):
        resized = cv2.resize(gray_img, dsize=(0, 0), fx=scale, fy=scale)

        r = gray_img.shape[1] / float(resized.shape[1])

        if resized.shape[0] < t_h or resized.shape[1] < t_w:
            break
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template_edged, cv2.TM_CCOEFF)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if not found:
            found.append((max_val, max_loc, r))

        if max_val > found[i][0]:
            found.append((max_val, max_loc, r))
            i += 1

    color_img = np.asarray(color_img)
    for f in found:
        _, max_loc, r = f
        start_x, start_y = int(max_loc[0] * r), int(max_loc[1] * r)
        end_x, end_y = int((max_loc[0] + t_w) * r), int((max_loc[1] + t_h) * r)
        cv2.rectangle(color_img, (start_x, start_y), (end_x, end_y), COLOR, 2)

    st.image(color_img)


if __name__ == "__main__":
    main()