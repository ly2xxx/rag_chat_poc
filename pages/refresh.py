import subprocess
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

# Define the path to the requirements.txt file
requirements_file = "requirements.txt"

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()

else:
    # Run pip install command
    try:
        subprocess.run(["pip", "install", "-r", requirements_file], check=True)
        print(f"Successfully installed dependencies from {requirements_file}.")
    except subprocess.CalledProcessError:
        print(f"Error installing dependencies from {requirements_file}.")
