import streamlit as st
import pandas as pd
import scraper.facebook_scraper as facebookscrape
import webdesign.design as design
import threading
import os
from datetime import datetime
import csv
import datetime as dt
import time


def select_option_buttons():

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        search_word = st.text_input('sökord', '')
    with col2:
        test_2 = st.button("test_2")
    with col3:
        test_3 = st.button("test_3")

    if test_3:
        st.write("works_3")
    elif test_2:
        st.write("works_2")
    elif test:
        st.write("works")


def main():
    design.select_option()


if __name__ == "__main__":
    main()
