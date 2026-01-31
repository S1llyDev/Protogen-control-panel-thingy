import json, subprocess, argon2

database = json.loads(execute(f'cat {DIR}', 1))