import socket
import base64
import sys

if "-v" in sys.argv:
    verbose_mode = 1
else:
    verbose_mode = 0 

def verbose(text):
    if verbose_mode == 1:
        print(text)
    else:
        pass

def remove_not_needed_slashes(var):
    verbose("remove_not_needed_slashes function started")
    while var.find("//") != -1:
        var = var.replace("//", "/")
        verbose(f"var = {var}")

    while var[0] == "/":
        var = var[1:]
        verbose(f"var = {var}")

    while var[-1] == "/":
        var = var[:-1]
        verbose(f"var = {var}")

    verbose("remove_not_needed_slashes function stopped")
    return(var)


try:
    argument = sys.argv[1]
    try:
        path = argument.split()[1][1:]
        clean_path = remove_not_needed_slashes(path)
        verbose(clean_path)
        clean_path = clean_path.replace("/", " ")
        verbose(clean_path)
        # execute("pbase {clean_path}") # pbase id nd3 set eye 1
    except(AttributeError):
        print("'NoneType' object has no attribute 'split'\n Make sure argument exists")
except(IndexError):
    print("List index out of range\n Make sure argument exists")
