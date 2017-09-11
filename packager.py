#!/usr/bin/python2.7

from textuilib import menu
from textuilib import menuItem
from textuilib import clear
from textuilib import choice
from textuilib import setHeader
from textuilib import displayHeader
from zipfile import ZipFile
from shutil import copyfile
import textuilib
import sys
import os
import py_compile
import time

setHeader("Python Packager ")

mainmenu = menu("Main Menu", [])
packmenu = menu("Package Directory", [])
testmenu = menu("Test Menu", [])
zipmenu = menu("Packaging Files...", [])

mainmenu.addMenuItem(menuItem("Package Directory", "pack"))
mainmenu.addMenuItem(menuItem("Quit", "quit"))

def main():
    #mainmenu.addMenuItem(textuilib.menuItem("Test Menu", "test"))
    clear()
    option = mainmenu.displayMenu()

    if option == "pack":
        pack(None)
    elif option == "packi":
        packi(None)
    elif option == "unpack":
        unpack()
    elif option == "quit":
        sys.exit()
    elif option == "test":
        test()
    else:
        main()

def pack(error):
    packmenu.clearMenuItems()
    clear()
    displayHeader(packmenu)
    if error == "1":
        print("That is not a valid directory! Make sure the directory you type ends with a '/'!")
    elif error == "2":
        print("No files could be packaged in that directory! Please enter another directory!")
    print("Enter the directory with the files to be packaged.")
    print("")
    option = raw_input("Directory: ")
    if os.path.isdir(option) == False:
        pack("1")
    else:
        if option[len(option) - 1] == "/":
            dirlist = os.listdir(option)
            files = {}
            tozip = []
            for file in dirlist:
                if file.endswith(".py"):
                    base = os.path.basename(file)
                    name = os.path.splitext(base)[0]
                    newfile = option + name + "-pack.py"
                    copyfile(file, newfile)
                    py_compile.compile(newfile)
                    os.remove(newfile)
                    newfile = option + name + "-pack.pyc"
                    os.rename(newfile, option + name + ".pyc")
                    #newfile = option + name + ".pyc"
                    newfile = name + ".pyc"
                    packmenu.addMenuItem(textuilib.menuItem(name, base))
                    files[base] = newfile
                    tozip.append(newfile)
                    #tozip.append(base)
            if files != {}:
                clear()
                displayHeader(packmenu)
                print("Select the script that should be run before the others.")
                print("")
                packmenu.displayOptions()
                option1 = choice(packmenu)

                mainfile = files.get(option1)
                print option1
                print mainfile
                base = os.path.basename(mainfile)
                name = os.path.splitext(base)[0]
                packageName = name
                os.rename(mainfile, option + "__main__.pyc")
                #print tozip
                tozip.remove(mainfile)
                tozip.append("__main__.pyc")
                packager(option, packageName, tozip)
                print tozip

            else:
                pack("2")
        else:
            pack("1")

def packager(option, packageName, tozip):
    clear()
    with ZipFile(option + packageName + ".pyp", "w") as zip:
        for file in tozip:
            zip.write(file)
            os.remove(file)
    displayHeader(packmenu)
    print("Success! Package saved as " + option + packageName + ".pyp")
    time.sleep(5)
    main()

main()
