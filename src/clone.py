import subprocess, shutil, time, os, stat
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_DIR = PROJECT_ROOT / "repos"
repo_url = os.getenv("REPO_URL")
repo_name = repo_url.split('/')[-1].replace(".git","")
repo_path = REPO_DIR / repo_name
try:
    subprocess.run(["git", "ls-remote", repo_url], check=True, capture_output=True, timeout=10, text=True)
    print("Verified github repository.")
    result = subprocess.run(["git", "clone", "--depth", "1", repo_url, str(repo_path)], capture_output=True, text=True, check=True)
    print(result.stdout)
except Exception as e:
    print("Error:", e)
print("Repository has been cloned.")

# operations

# def remove_readonly(func, path, exc_info):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)
# print(repo_path.exists())
# shutil.rmtree(repo_path, onexc=remove_readonly)
# print("Repository has been removed.")