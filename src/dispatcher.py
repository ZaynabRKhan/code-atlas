# import ast, tomllib, configparser, yaml, json
# from markdown_it import MarkdownIt
# from markdown_it.tree import SyntaxTreeNode
import tree_sitter_javascript as tsjs
import tree_sitter_python as tsp
import tree_sitter_typescript as tsts
import tree_sitter_json as tsj
import tree_sitter_markdown as tsmd
import tree_sitter_toml as  tstm
import tree_sitter_yaml as tsy
from tree_sitter import Language
from tree_sitter import Parser as TSParser
import configparser
from docutils import frontend, utils
from docutils.parsers.rst import Parser as RSTParser

class Dispatcher:
    def __init__(self, files):
        self.files = files
        self.python_files = []
        self.js_files = []
        self.ts_files = []
        self.md_files = []
        self.rst_files = []
        self.txt_files = []
        self.toml_files = []
        self.cfg_files = []
        self.yml_files = []
        self.json_files = []
        self.parser = Parser()
        print("inti done")

    def dispatchFiles(self):
        for file in self.files:
            ext = "." + str(file).split(".")[-1]
            match ext:
                case ".py" | ".pyi":
                    self.python_files.append(file)
                    print("matched python")
                case ".js" :
                    self.js_files.append(file)
                    print("matched js")
                case ".ts":
                    self.ts_files.append(file)
                case ".md":
                    self.md_files.append(file)
                    print("matched md")
                case ".rst":
                    self.rst_files.append(file)
                    print("matched rst")
                case ".txt":
                    self.txt_files.append(file)
                    print("matched txt")
                case ".toml":
                    self.toml_files.append(file)
                    print("matched toml")
                case ".cfg" | ".ini":
                    self.cfg_files.append(file)
                    print("matched cfg or ini")
                case ".yml" | ".yaml":
                    self.yml_files.append(file)
                    print("matched yml or yaml")
                case ".json":
                    if file.name not in {"package-lock.json"}:
                        self.json_files.append(file)
                        print("matched json")
                
        if self.python_files: self.parser.parseTreeSitters(self.python_files)
        if self.js_files: self.parser.parseTreeSitters(self.js_files)
        if self.ts_files: self.parser.parseTreeSitters(self.ts_files)
        if self.md_files: self.parser.parseTreeSitters(self.md_files)
        if self.toml_files: self.parser.parseTreeSitters(self.toml_files)
        if self.yml_files: self.parser.parseTreeSitters(self.yml_files)
        if self.json_files: self.parser.parseTreeSitters(self.json_files)
        if self.rst_files: self.parser.parseRst(self.rst_files)
        if self.txt_files: self.parser.parseTxt(self.txt_files)
        if self.cfg_files: self.parser.parseCfg(self.cfg_files)
        print("added files")

    def getParsedCode(self):
        return self.parser.getCode()

class Parser:
    def __init__(self):
        self.parsers = {
            "py": TSParser(Language(tsp.language())),
            "js": TSParser(Language(tsjs.language())),
            "ts": TSParser(Language(tsts.language_typescript())),
            "md": TSParser(Language(tsmd.language())),
            "toml": TSParser(Language(tstm.language())),
            "yml": TSParser(Language(tsy.language())),
            "yaml": TSParser(Language(tsy.language())),
            "json":TSParser(Language(tsj.language())),
        }
        self.code = {
            "py": {},
            "js": {},
            "ts": {},
            "md": {},
            "rst": {},
            "txt": {},
            "toml": {},
            "cfg": {},
            "yml": {},
            "yaml": {},
            "json":{}
        }

    def parseTreeSitters(self, files):
        for file in files:
            ext = file.suffix.lstrip(".")
            parser = self.parsers[ext]
            with open(file, "rb") as f:
                self.code[ext][file.name] = parser.parse(f.read())

    def parseTxt(self, files):
        for file in files:
            self.code["txt"][file.name] = open(file).read()

    def parseRst(self, files):
        settings = frontend.get_default_settings(RSTParser)
        rst_parser = RSTParser()
        for file in files:
            with open(file, encoding="utf-8") as f:
                document = utils.new_document(f.name, settings)
                rst_parser.parse(f.read(), document)
            self.code["rst"][file.name] = document

    def parseCfg(self, files):
        for file in files:
            config = configparser.ConfigParser()
            try:
                with open(file, "r", encoding="utf-8") as f:
                    config.read_file(f)
            except (configparser.Error, UnicodeDecodeError):
                with open(file, "r") as f:
                    config = f.read()
                self.code["cfg"][file.name] = config

    def getCode(self):
            return self.code

    # def parsePython(self, files):
    #     language = Language(tsp.language())
    #     pyparser = TSParser(language)
    #     for file in files:
    #         with open(file, "rb") as f:
    #             self.code["py"][file.name] = pyparser.parse(f.read())

    # def parseJs(self, files):
    #     language = Language(tsjs.language())
    #     jsparser = TSParser(language)
    #     for file in files:
    #         with open(file, "rb") as f:
    #             self.code["js"][file.name] = jsparser.parse(f.read())

    # def parseToml(self, files):
    #     language = Language(tstm.language())
    #     tmparser = TSParser(language)
    #     for file in files:
    #         with open(file, "rb") as f:
    #             self.code["js"][file.name] = tmparser.parse(f.read())

    # def parseMd(self, files):
    #     md = MarkdownIt()
    #     for file in files:
    #         tokens = md.parse(open(file).read())
    #         self.code["md"][file.name] = SyntaxTreeNode(tokens)
        
    # def parseYml(self, files):
    #     for file in files:
    #         with open(file, "r", encoding="utf-8") as f:
    #             doc = yaml.safe_load(f)
    #         if doc is None:
    #             with open(file, "r", encoding="utf-8") as f:
    #                 doc = f.read()
    #         self.code["yml"][file.name] = doc

    # def parseJson(self, files):
    #     for file in files:
    #         with open(file, "r", encoding="utf-8") as f:
    #             self.code["json"][file.name] = json.load(f)
