# Import requests and subprocess libraries
import requests
import subprocess
import os


# Define a function to run a git command and return the output
def run_git_command(command):
    # Use subprocess.run to execute the command and capture the output
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except:
    	return
    # Check if the command was successful
    if result.returncode == 0:
        # Return the output as a string
        return result.stdout.strip()
    #else:
        # Raise an exception with the error message
        # raise Exception(result.stderr.strip())

# Define a function to copy a file from a commit to a destination folder
def copy_file_from_commit(commit, file, dest):
    # Use git show to get the content of the file at the commit
    content = run_git_command(f"git show {commit}:{file}")
    # Open the destination file in write mode
    if isinstance(content, str):
        with open(dest, "w") as f:
            # Write the content to the file
            f.write(content)

def get_directory_path(path):
    # Split the path into a list of components
    components = path.split('/')

    # Remove the last component, which is the file name
    components.pop()

    # Join the remaining components with slashes
    directory_path = '/'.join(components)

    # Return the directory path
    return directory_path

# Define a function that takes a github commit url as input
def list_changed_files(commit_url):
    # Extract the owner, repo, and sha from the url
    # Example: https://github.com/microsoft/vscode/commit/8f3d425d5c9c2685f5b8c063a5f0f8a9f2f8f83f
    # owner = microsoft, repo = vscode, sha = 8f3d425d5c9c2685f5b8c063a5f0f8a9f2f8f83f
    owner, repo, _, sha = commit_url.split('/')[-4:]

    # Construct the API endpoint to get the commit details
    # Example: https://api.github.com/repos/microsoft/vscode/commits/8f3d425d5c9c2685f5b8c063a5f0f8a9f2f8f83f
    api_url = f'https://api.github.com/repos/{owner}/{repo}/commits/{sha}'

    # Make a GET request to the API endpoint and get the JSON response
    response = requests.get(api_url).json()

    # Get the list of files that were changed in the commit
    try:
        files = response['files']
    except:
        print("here")
        return

    # Print the number of files that were changed
    print(f'{len(files)} files changed in this commit.')

    # Loop through the files and print their names and statuses
    for file in files:
        print(f'{file["filename"]} - {file["status"]}')

    # Construct the clone url for the repository
    # Example: https://github.com/microsoft/vscode.git
    clone_url = f'https://github.com/{owner}/{repo}.git'

    path = "repo/" + repo

    # Clone the repository to the current directory using subprocess
    subprocess.run(['git', 'clone', clone_url, path])

    # Print a message to indicate the cloning is done
    print(f'Repository {repo} cloned successfully.')
    
    # Get the commit and repository path from the command line arguments
    commit = sha

    # Change the current working directory to the repository path
    os.chdir(path)

    # Get the previous commit using git rev-parse
    prev_commit = run_git_command(f"git rev-parse {commit}^")


    logs = []

    for file in files:
        dest = file["filename"].split("/").pop()
        
        # Copy the file from the previous commit to the before folder
        copy_file_from_commit(prev_commit, file["filename"], "../../before/" + dest)

        # Copy the file from the specified commit to the after folder
        copy_file_from_commit(commit, file["filename"], "../../after/" + dest)
        
        logs.append(commit_url + "," + dest)
    
    os.chdir("../../")
    
    with open("output.csv", "a") as f:
        f.write("\n")
        f.write("\n".join(logs))

urls = """commit links goes here """

# Split the input by newline character and store it in a list
url_list = urls.split("\n")

# Loop through the list and pass each url to the parser function
for url in url_list:
    list_changed_files(url)
