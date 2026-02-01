from http.server import BaseHTTPRequestHandler, HTTPServer
from fastapi.middleware.cors import CORSMiddleware
from argon2.exceptions import VerifyMismatchError
from argon2.exceptions import InvalidHashError
import subprocess, threading, sys, json, os
from fastapi import FastAPI, HTTPException
from socketserver import ThreadingMixIn
from argon2 import PasswordHasher

DIR = "/home/kommit/Projects/Protogen/Web-Panel/database"

hashes_path = os.path.expanduser(os.path.expandvars('$PG_WEB_PANEL/passHashes'))
ph = PasswordHasher()



if "-v" in sys.argv:
    verbose_mode = 1
    print(sys.argv)
    v_index = sys.argv.index("-v")
    sys.argv.pop(v_index)
    try:    
        v_index = sys.argv.index(f"{__name__}.py")
    except(ValueError):
        try:
            v_index = sys.argv.index(f"{__name__}")
        except:
            print("Unexcepted error")
            sys.exit(-1)
    sys.argv.pop(v_index)
    del v_index
    print(sys.argv)
else:
    verbose_mode = 0


def verbose(text):
    if verbose_mode == 1:
        print(text)
    else:
        return

def execute(cmd, output_capturing):
    if output_capturing == 1:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        verbose(f"Executed {cmd}")
        verbose(result.stdout.strip())
        return result.stdout.strip()
    else:
        subprocess.run(cmd, shell=True, capture_output=False, text=True)
        verbose(f"Executed {cmd}")

def read(file):
    return(execute(f"cat {file}", 1))
    



def passCheck(_id, password):
    try:
        int(_id)
    except ValueError:
        print("ID is not a number")
        sys.exit(3)
    try:
        _hash = json.dumps(json.loads(read(f'{DIR}/pbase.json'))['1']['hash'])[1:][:-1]
        verbose(_hash)
    except(KeyError):
        print(f"User with ID {_id} not found in file")
        sys.exit(3)
    try:
        ph.verify(_hash, password)
        return(1)
    except VerifyMismatchError:
        print("Invalid password")
        return(0)
    except InvalidHashError:
        print("Invalid hash")
        sys.exit(4)




class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        verbose(self.path)
        if self.path == '/' or self.path == '/ ':
            self.path = '/web/index.html'

        if self.path == '/preview':
            self.path = '/web/preview.html'

        try:
            with open('.' + self.path, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Unknown request')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        verbose(self.path)
        if self.path != '/api?config':
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8')
        verbose(f"Length: {content_length}, Body: {post_body}")
        
        try:
            data = json.loads(post_body)
            verbose(f"Parsed: {data}")
        except json.JSONDecodeError:
            self.send_response(400, "Invalid JSON")
            self.end_headers()
            return
        
        # Auth check
        if passCheck(data.get('username'), data.get('password')) == 0:
            self.send_response(401, "Auth failed")
            self.end_headers()
            return
        
        # FIXED: Send full config for user "1" (Kommit)
        try:
            db_content = read(f'{DIR}/pbase.json')  # Fixed path
            db = json.loads(db_content)
            user_config = db['1']['config']  # Matches your JSON structure
            verbose(user_config)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "config": user_config}).encode())
        except Exception as e:
            verbose(f"Config error: {e}")
            self.send_response(500, "Config error")
            self.end_headers()




class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    try:
        address = "localhost:4554"
        address1= str(address.split(":")[0])
        address2= int(address.split(":")[1])
        server = ThreadedHTTPServer((f'{address1}', address2), Handler)
        print(f'Starting server on http://{address} use <Ctrl-C> to stop')
        server.serve_forever()
    except(KeyboardInterrupt):
        print("\nStopping server")
        sys.exit(0)