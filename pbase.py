import subprocess
import shlex
import sys

def execute(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)

try:
    _dir = sys.argv[1]
except(IndexError):
    print("Usage: pbase [dir]")
    sys.exit(1)

if _dir[-1] == "/":
    _dir = _dir[:-2] # Just in case remove every "/" at the end of path
    pass

execute(f'mkdir -p {_dir}')
print(f'Ran mkdir -p {_dir}')

execute(f'echo "3" > {_dir}/mod_jaws')
print(f'Ran echo "3" > {_dir}/mod_jaws')

execute(f'echo "0" > {_dir}/mod_eye')
print(f'Ran echo "0" > {_dir}/mod_eye')

execute(f'echo "4" > {_dir}/mod_nose')
print(f'Ran echo "4" > {_dir}/mod_nose')

execute(f'echo "3" > {_dir}/mod_owo')
print(f'Ran echo "3" > {_dir}/mod_owo')

execute(f'echo "3" > {_dir}/mod_zloy')
print(f'Ran echo "3" > {_dir}/mod_zloy')

execute(f'echo "1" > {_dir}/mod_kill')
print(f'Ran echo "1" > {_dir}/mod_kill')

execute(f'echo "3" > {_dir}/alt_owo')
print(f'Ran echo "3" > {_dir}/alt_owo')

execute(f'echo "3" > {_dir}/alt_ang')
print(f'Ran echo "3" > {_dir}/alt_ang')

execute(f'echo "1" > {_dir}/alt_kill')
print(f'Ran echo "1" > {_dir}/alt_kill')