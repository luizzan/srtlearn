import os
from configparser import ConfigParser
from googletrans import Translator
import streamlit as st
from streamlit import caching
from utils import *

config = ConfigParser()
translator = Translator()

CONFIG_FILE = './config/config.ini'
config.read(CONFIG_FILE)
DATA_PATH = config['general'].get('data_path', './data')
LOAD_LOCAL_STR = 'Load local files'
N_FILES = 2

# ==================================================
# CLEAR CACHE FUNCTIONS
# ==================================================

@st.cache(suppress_st_warning=True)
def load_srt_files(files):
    data = []
    for f in files:
        data += [srt_to_df(f)]

    return data

@st.cache(suppress_st_warning=True)
def translate(word, src, dest):
    try:
        translation = 'Translation: ' + translator.translate(word, src=src, dest=dest).text
    except Exception as e:
        translation = 'Check your language codes and input text.'
    return translation


# ==================================================
# MAIN TEXT
# ==================================================

st.title('Subtitle reader')
st.sidebar.title('Select sources')

# ==================================================
# SIDEBAR
# ==================================================

ls_folders = [LOAD_LOCAL_STR] + sorted(os.listdir(DATA_PATH))
folder = st.sidebar.selectbox('Select movie', ls_folders)

files = []
if folder == LOAD_LOCAL_STR:
    for i in range(N_FILES):
        f = st.sidebar.file_uploader('Select subtitle file', type='srt', key=f'srt{i}')
        files += [f]
else:
    ls_files = sorted(os.listdir(f'{DATA_PATH}/{folder}'))
    for i in range(N_FILES):
        f = st.sidebar.selectbox('Select subtitle file', ls_files, index=i)
        f = f'{DATA_PATH}/{folder}/{f}'
        files += [f]

files = [i for i in files if i is not None]

lag = st.sidebar.number_input('Lag', value=0)
# TODO add lag per file

# ==================================================
# MAIN PAGE
# ==================================================

if len(files) < 2:
    st.write('Select files.')
else:
    data = load_srt_files(files)

    line_number = st.number_input('Line', value=0)

    # Original line
    line1 = min(max(line_number, 0), len(data[0])-1)
    st.text(data[0][line1])

    # Translation placeholders
    trans_lines = []
    for i in data[1:]:
        trans_lines += [st.empty()]

    # Hide translation checkbox
    is_hide = st.checkbox('Hide translation', value=False)

    # Write translation lines
    for i, l in enumerate(trans_lines):
        if is_hide:
            l.text('----------')
        else:
            linei = min(max(line_number+lag, 0), len(data[i+1])-1)
            l.text(data[i+1][linei])

# ==================================================
# TRANSLATE
# ==================================================

st.sidebar.title('Translation')
trans_src = st.sidebar.text_input('Input language', 'cs')
trans_dest = st.sidebar.text_input('Output language', 'en')

st.write('')
st.write('')
st.write('')
st.markdown("""**Translate** (powered by Google Translate)""")
text = st.text_input('Input text')
translation = translate(text, trans_src, trans_dest)
st.write(translation)
