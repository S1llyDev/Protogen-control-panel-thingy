import subprocess
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

def execute(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)

try:
    _dir = sys.argv[1]
except(IndexError):
    print("Usage: pbase [dir]")
    sys.exit(1)

while _dir[-1] == "/":
    verbose(f"{_dir} => {_dir[:-1]}")
    _dir = _dir[:-1]
    pass

execute(f'mkdir -p {_dir}')
verbose(f'Ran mkdir -p {_dir}')

execute(f'echo "3" > {_dir}/mod_jaws')
verbose(f'Ran echo "3" > {_dir}/mod_jaws')

execute(f'echo "0" > {_dir}/mod_eye')
verbose(f'Ran echo "0" > {_dir}/mod_eye')

execute(f'echo "4" > {_dir}/mod_nose')
verbose(f'Ran echo "4" > {_dir}/mod_nose')

execute(f'echo "3" > {_dir}/mod_owo')
verbose(f'Ran echo "3" > {_dir}/mod_owo')

execute(f'echo "3" > {_dir}/mod_zloy')
verbose(f'Ran echo "3" > {_dir}/mod_zloy')

execute(f'echo "1" > {_dir}/mod_kill')
verbose(f'Ran echo "1" > {_dir}/mod_kill')

execute(f'echo "3" > {_dir}/alt_owo')
verbose(f'Ran echo "3" > {_dir}/alt_owo')

execute(f'echo "3" > {_dir}/alt_ang')
verbose(f'Ran echo "3" > {_dir}/alt_ang')

execute(f'echo "1" > {_dir}/alt_kill')
verbose(f'Ran echo "1" > {_dir}/alt_kill')