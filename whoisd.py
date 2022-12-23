# WHOISD: who is data
import base64
import github3
from rich import print as rprint
import time

def github_connect():
    '''
    Connect to the github client and correct repository
    '''

    with open("./mytoken.txt") as f:
        token = f.read()
    user = "vanHooijdonkC"
    sess = github3.login(token=token)
    return sess.repository(user, "EH8")


def get_file_contents(file, repo):
    '''
    returns all the files in the given repository
    '''

    b64_data = repo.file_contents("data/" + file).content
    data = base64.b64decode(b64_data)
    datadata = base64.b64decode(data)

    return datadata


def prettyprint(filecontents):
    '''
    Pretty print all the contents of the files with library rich
    '''

    for x in filecontents:
        if filecontents.index(x) % 2 == 0:
            rprint(f"\tcontents of file [bold red]{x}[/bold red]:")
        else:
            try:
                rprint(f"{x}\n")
                time.sleep(2)
            except:
                print("this file contains a photo! \n")


def main():
    contents = []
    try:
        print("[*] Attempting to retrieve the data")
        repo = github_connect()
        dirContent = repo.directory_contents("data/")

        if dirContent is not None:
            for x in dirContent:
                contents.append(x[0])
                contents.append(get_file_contents(x[0], repo))
        else:
            print("try again, no data found yet")

    except Exception as e:
        print(e)
        print("[x] Failed import of the data")

    prettyprint(contents)


if __name__ == "__main__":
    main()
