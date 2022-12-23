import pyscreenshot as ImageGrab


def run(*args):
    print(args)
    print("[*] In module screenshot")
    img = ImageGrab.grab()
    img.save("./temp.png")

    with open("./temp.png", "rb") as img:
        stringimg = img.read()
        return stringimg
