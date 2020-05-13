import os
from configparser import ConfigParser
import streamlit as st
from streamlit import caching
from utils import *

config = ConfigParser()

CONFIG_FILE = './config/config.ini'
config.read(CONFIG_FILE)
DATA_PATH = config['general'].get('data_path', './data')

# ==================================================
# FUNCTIONS
# ==================================================

@st.cache
def load_srt_files(file1, file2):

    data1 = srt_to_df(f'{DATA_PATH}/{folder}/{file1}')
    data2 = srt_to_df(f'{DATA_PATH}/{folder}/{file2}')

    return data1, data2

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title('Select sources')

ls_folders = os.listdir(DATA_PATH)
folder = st.sidebar.selectbox('Select movie', ls_folders)

ls_files = os.listdir(f'{DATA_PATH}/{folder}')
file1 = st.sidebar.selectbox('Select first subtitle file', ls_files, index=0)
file2 = st.sidebar.selectbox('Select second subtitle file', ls_files, index=1)

lag = st.sidebar.number_input('Lag', value=0)

# ==================================================
# MAIN PAGE
# ==================================================

st.title('Subtitle reader')

data1, data2 = load_srt_files(file1, file2)

line_number = st.number_input('Line', value=0)

line1 = min(max(line_number, 0), len(data1)-1)
st.text(data1[line1])

line2_ui = st.empty()

is_hide_translation = st.checkbox('Hide translation', value=False)

if is_hide_translation:
    line2_ui.text('----------')
else:
    line2 = min(max(line_number+lag, 0), len(data2)-1)
    line2_ui.text(data2[line2])