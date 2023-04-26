import os
from datetime import datetime
import re
import streamlit as st

def case_gilla_stort_fan(comment_list, comment):
    st.write(comment_list[comment + 5])
    st.write(comment_list[comment + 6])


def case_gilla_mest_relevanta(comment_list, comment):
    st.write(comment_list[comment + 6])
    st.write(comment_list[comment + 7])


def case_gilla(comment_list, comment):
    if 'gilla-markeringar' in comment_list[comment + 4]:
        return None
    elif "Stort fan\n" == comment_list[comment + 4]:
        case_gilla_stort_fan(comment_list, comment)
    elif "Mest relevanta\n" == comment_list[comment + 4]:
        case_gilla_mest_relevanta(comment_list, comment)
    else:
        st.write(comment_list[comment + 4])
        st.write(comment_list[comment + 5])


def calculate_current_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    current_date = dt_string[-8:len(dt_string)]
    st.write(current_date)


def case_tim(comment_list, comment):
    if comment_list[comment][-5]:
        try:
            int(comment_list[comment][-6])
            st.write(comment_list[comment+2])
            calculate_current_date()
        except ValueError:
            return None
    else:
        return None

    #if comment_list[comment][-4:-1]:

def case_day():
    print("")


def case_finder(comment_list):
    day_pattern = r"\d+ d"
    cleaned_comment_list = []
    for comment in range(0, len(comment_list)):
        if comment_list[comment] == "Gilla\n":
            case_gilla(comment_list, comment)
        if "tim" in comment_list[comment]:
            case_tim(comment_list, comment)
        if re.search(day_pattern, comment_list[comment]):
            st.write(re.search(day_pattern, comment_list[comment]).group())


def get_str_from_txt_file(txt_file_dir):
    unfiltered_comments = []
    try:
        with open(txt_file_dir, 'r') as f:
            for line in f:
                unfiltered_comments.append(line)
    except FileNotFoundError:
        st.write("File not found.")

    case_finder(unfiltered_comments)
    return unfiltered_comments


def main(txt_file_dir):
    st.write(txt_file_dir)
    st.write("it's here")
    unfiltered_comments = get_str_from_txt_file(txt_file_dir)

