from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
import subprocess
import sys
import os

ph = PasswordHasher()

if "-v" in sys.argv:
    verbose_mode = 1
else:
    verbose_mode = 0

def execute(cmd, output_capturing):
    cmd = f"bash -c {subprocess.list2cmdline([cmd])}" if "~" in cmd else cmd
    
    if output_capturing == 1:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        verbose(result.stdout.strip())
        return result.stdout.strip()
    else:
        subprocess.run(cmd, shell=True, capture_output=False, text=True)

def verbose(text):
    if verbose_mode == 1:
        print(text)

verbose(os.environ.get('PG_WEB_PANEL'))

def remove_not_needed_slashes(var):
    verbose("remove_not_needed_slashes function started")
    while var.find("//") != -1:
        var = var.replace("//", "/")
    while var.startswith("/"):
        var = var[1:]
    while var.endswith("/"):
        var = var[:-1]
    verbose("remove_not_needed_slashes function stopped")
    return var

def change_file(_id, var, value):
    raw_path = f"$PG_WEB_PANEL/pg_dbase/{_id}/{var}"
    full_path = os.path.expanduser(os.path.expandvars(raw_path))
    
    if os.path.exists(full_path):
        execute(f'echo "{value}" > {raw_path}', 0)
        verbose(f'Ran echo "{value}" > {raw_path}')
    else:
        print(f"Invalid path: {full_path}")
        sys.exit(2)

def checkPass(_id, password):
    try:
        int(_id)
    except ValueError:
        print("ID is not a number")
        sys.exit(3)

    file_path = os.path.expanduser(os.path.expandvars("$PG_WEB_PANEL/passHashes"))
    line = execute(f"grep '^{_id}|' {file_path}", 1)

    if not line:
        print(f"User with ID {_id} not found in file")
        sys.exit(3)

    try:
        hash_part = line.split("|")[1]
        ph.verify(hash_part, password)
        return 1
    except VerifyMismatchError:
        print("Invalid password")
        sys.exit(4)
    except Exception as e:
        verbose(f"Unexpected error: {e}")
        sys.exit(5)

try:
    args_without_flags = [a for a in sys.argv[1:] if a != "-v"]
    if not args_without_flags:
        sys.exit(1)
        
    req = args_without_flags[0]
    verbose(f"Request = {req}")

    parts = req.split()
    raw_path = parts[1]

    clean_path = remove_not_needed_slashes(raw_path)
    path_list = clean_path.split("/")

    _id = path_list[0]
    password = path_list[1]
    action = path_list[2]
    var = path_list[3]
    value = path_list[4]

    if action == "SET":
        if checkPass(_id, password) == 1:
            change_file(_id, var, value)
    elif action == "GET":
        sys.exit(0)

except (ValueError, IndexError):
    sys.exit(1)
