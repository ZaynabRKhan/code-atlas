import os
from dotenv import load_dotenv
from loader import LoadCode
from dispatcher import Dispatcher
from graph_creation import TreeTraversal

load_dotenv()
repo_code = LoadCode(os.getenv("REPO_URL"))
repo_code.traverseFiles(os.getenv("REPO_DIR"))
repo_code.showFiles()

dispatcher = Dispatcher(repo_code.showFiles())
dispatcher.dispatchFiles()
code = dispatcher.getParsedCode()

with open("code_output.txt", "w") as f:
    f.write(str(code))

# traversal = TreeTraversal(code)
# traversal.traversePython()