import streamlit as st
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
import base64
import shutil
from datetime import datetime

def create_download_zip(zip_directory, zip_path):
    """ 
        zip_directory (str): path to directory  you want to zip 
        zip_path (str): where you want to save zip file
        filename (str): download filename for user who download this
    """
    shutil.make_archive(zip_path, 'zip', zip_directory)
    filename = zip_path+".zip"
    with open(filename, 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download=\'{filename}\'>\
            vectors \
        </a>'
        st.markdown(href, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | dl🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()

else:
    current_datetime = datetime.now().strftime("pkl-%d%m%Y.%H.%M.%S")
    create_download_zip("embeddings", current_datetime)