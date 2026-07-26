import os
from pathlib import Path
from dotenv import load_dotenv, set_key

load_dotenv()

class LoadCode:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.files = []
        repo_name = self.repo_url.split('/')[-1].replace(".git","")
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        REPO_DIR = PROJECT_ROOT / "repos" / repo_name
        self.repo_dir = REPO_DIR
        set_key(".env", "REPO_DIR", str(REPO_DIR), quote_mode="never")
    def getFiles(self, subdir):
        self.files.append(subdir)
    def traverseFiles(self, repo_dir):
        if repo_dir is None:
            return self.files
        for subdir in Path(repo_dir).iterdir():
            if ".git" in subdir.parts or ".gitignore" in subdir.parts:
                continue
            if subdir.is_file():
                self.getFiles(subdir)
            elif subdir.is_dir():
                self.traverseFiles(subdir)
    def showFiles(self):
       return self.files