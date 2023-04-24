import streamlit as st

from lab_01 import gauss_blur
from lab_02 import binary
from lab_03 import math_morph



st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Basil Tkachenko](https://github.com/Basilt69)
        for **Introduction to Computer vision labs**
        in [BMSTU](https://bmstu.ru) 
    """

    st.header("BMSTU, University department: Informatics and software development - 7")
    st.markdown("**Course title:** Introduction to computer vision")
    st.markdown("**University lecturer**: Kivva K.A.")
    st.markdown("**Student:** Tkachenko B.M.")
    st.sidebar.markdown(author)


def main():
    header()
    lab = st.sidebar.radio(
        "Select your lab:", (
            "1. Gaussian blur",
            "2. Binarisation",
        ),
        index=1
    )

    if lab[:1] == "1":
        gauss_blur.main()

    elif lab[:1] == "2":
        binary.main()

    elif lab[:1] == "3":
        math_morph.main()



if __name__ == "__main__":
    main()
