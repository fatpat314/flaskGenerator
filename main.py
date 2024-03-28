import os
import subprocess
from flaskGen import create_flask_file
from dockerGen import create_dockerfile
from requirementsGen import create_requirements

def create_empty_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Empty directory '{directory_path}' created successfully.")
    except OSError as error:
        print(f"Error creating directory '{directory_path}': {error}")

def run_docker_build(directory_name):
    try:
        # Run the 'docker info' command
        result = subprocess.run(['docker', 'build', '-t', 'flask-hello-world', f'./{directory_name}'], capture_output=True, text=True, check=True)
        
        # Check if the command ran successfully
        if result.returncode == 0:
            # Print the output
            print(result.stdout)
        else:
            print("Command failed with return code:", result.returncode)
            print("Error message:", result.stderr)
    except subprocess.CalledProcessError as e:
        # If there's an error, print the error message
        print("Error:", e)

# Create Empty Directory:
directory_name = "flask_test"
directory_path = f"./{directory_name}"
create_empty_directory(directory_path)

#  Create Flask file
filename = "main.py"
filepath = f"./{directory_name}/{filename}"
flask_code = create_flask_file(filepath)

# Create requirements.txt
filename = "requirements.txt"
filepath = f"./{directory_name}/{filename}"
requirements = create_requirements(filepath, flask_code)

# Create Dockerfile
filename = "Dockerfile"
filepath = f"./{directory_name}/{filename}"
create_dockerfile(filepath, flask_code, requirements)

# Run docker build
run_docker_build(directory_name)




