import subprocess

# Define the path to the requirements.txt file
requirements_file = "requirements.txt"

# Run pip install command
try:
    subprocess.run(["pip", "install", "-r", requirements_file], check=True)
    print(f"Successfully installed dependencies from {requirements_file}.")
except subprocess.CalledProcessError:
    print(f"Error installing dependencies from {requirements_file}.")
