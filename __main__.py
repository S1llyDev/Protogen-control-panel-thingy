from http.server import BaseHTTPRequestHandler, HTTPServer
from fastapi.middleware.cors import CORSMiddleware
from argon2.exceptions import VerifyMismatchError
import subprocess, threading, sys, json, os
from fastapi import FastAPI, HTTPException
from socketserver import ThreadingMixIn
from argon2 import PasswordHasher

DIR = "/home/kommit/Projects/Protogen/Web-Panel/database/"

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
        sys.exit(-1)




class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        verbose(self.path)
        if self.path == '/' or self.path == '/ ':
            self.path = '/web/index.html'
        if self.path == '/preview':
            self.path = '/web/preview.html'
        
            # path = self.path
            # while path.find('//') != -1:
            #     self.path=path.replace('//', '/')
            # while path[0] == '/':
            #     path=path[1:]
            # while path[-1] == '/':
            #     path=path[:-1]
            # self.path = path
            # path = self.path.split("/")
            # if path[0] == 'SET':
            #     SET(path[1],path[2],path[3],path[4],self)
            # elif path[0] == 'GET':
            #     GET(path[1],path[2],path[3],self)
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
        path_split = self.path[1:].split("/")
        verbose(path_split)
        content_length = int(self.headers.get('Content-Length', 0))
        verbose(content_length)
        post_body_string = self.rfile.read(content_length).decode('utf-8')
        verbose(post_body_string)
        content_type = self.headers.get('Content-Type', '')
        data = {}
        if 'application/json' in content_type:
            try:
                data = json.loads(post_body_string)
            except json.JSONDecodeError:
                print("Error parsing JSON")
        else:
            print(f"Received raw data of type {content_type}: {post_body_string}")


        print(f"Received POST data: {data}")
        verbose(self.path)

        content_length = int(self.headers.get('Content-Length', 0))
        verbose(content_length)
        post_body_string = self.rfile.read(content_length).decode('utf-8')
        verbose(post_body_string)
        content_type = self.headers.get('Content-Type', '')
        data = {}
        if 'application/json' in content_type:
            try:
                data = json.loads(post_body_string)
            except json.JSONDecodeError:
                print("Error parsing JSON")
        else:
            print(f"Received raw data of type {content_type}: {post_body_string}")


            print(f"Received POST data: {data}")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_message = "{ }"
            self.wfile.write(response_message.encode("utf-8"))






        if self.path == '/api?config': # /api?config/VAR/VALUE
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_message = json.dumps(json.loads(read(f"{DIR}pbase.json"))['1']['config'])
            verbose(json.dumps(json.loads(read(f"{DIR}pbase.json"))['1']['config']))
            verbose(json.dumps(json.loads(read(f"{DIR}pbase.json"))['1']['config']).encode('utf-8'))
            # verbose(read(f"{DIR}/pbase.json"))
            # response_message = '1'
            self.wfile.write(response_message.encode("utf-8"))

        # database = json.loads(execute(f'cat {DIR}/{self.path.split("/")[1]}', 1))
        # try:
        #     with open('.' + self.path, 'rb') as f:
        #         content = f.read()
        # except FileNotFoundError:
        #     if self.path.split("/") != 'SET' or self.path.split("/") != 'GET':
        #         self.send_response(404)
        #         self.end_headers()
        #         self.wfile.write(b'Unknown request')
        #     return
        
        # self.send_response(200)
        # self.send_header('Content-Type', 'text/html')
        # self.end_headers()
        # self.wfile.write(content)


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