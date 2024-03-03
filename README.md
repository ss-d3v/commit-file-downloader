# Commit-file-downloader
Takes github commit urls as input to download the previous and current version of all files related to that commit.

## Prerequisites
- [Git](https://github.com/git-guides/install-git)
- [Python3](https://www.python.org/downloads/)

## Usage
Edit commit links in the script and run:
```bash
python3 main.py
```

## Output
- `before/`: previous version of a file
- `after/`: version of file after commit
- `repo/`: repositories cloned here
- `output.csv`: containes commit link and files names 
