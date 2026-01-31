use std::{
    env,
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    path::Path,
    thread,
    process::Command,
};

fn main() {
    let listener = TcpListener::bind("0.0.0.0:8888").unwrap();
    Command::new("clo")
        .arg("start")
        .arg("$CLO_UUID_PBASE")
        .spawn()
        .expect("There was an issue with clo");

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        thread::spawn(|| {
            handle_connection(stream);
        });
    }
}

fn handle_connection(mut stream: TcpStream) {    
    let mut buf_reader = BufReader::new(&stream);
    let mut request_line = String::new();
    if let Err(_) = buf_reader.read_line(&mut request_line) { return; }

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() < 2 { return; }
    
    let path = parts[1];
    let path_segments: Vec<&str> = path.split('/').filter(|s| !s.is_empty()).collect();

    // Python запускается всегда для любой обработки логики
    Command::new("python")
        .arg("py/http_request_handler.py")
        .arg(request_line.trim())
        .spawn()
        .expect("Failed to run Python");

    if path_segments.len() >= 4 {
        let id = path_segments[0];
        let action = path_segments[2]; // GET или SET
        let var = path_segments[3];

        if action == "SET" {
            let response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\nContent-Type: text/plain\r\n\r\nOK";
            let _ = stream.write_all(response.as_bytes());
            return;
        }

        if action == "GET" {
            let base_path = env::var("PG_WEB_PANEL").unwrap_or_else(|_| "/home/kommit/Projects/Protogen/Web-Panel/".to_string());
            let file_path = Path::new(&base_path).join("pg_dbase").join(id).join(var);

            match fs::read(&file_path) {
                Ok(contents) => {
                    let response_header = format!(
                        "HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n",
                        contents.len()
                    );
                    let _ = stream.write_all(response_header.as_bytes());
                    let _ = stream.write_all(&contents);
                }
                Err(_) => {
                    let response = "HTTP/1.1 404 NOT FOUND\r\nContent-Length: 0\r\n\r\n";
                    let _ = stream.write_all(response.as_bytes());
                }
            }
            return;
        }
    }

    let (status_line, filename) = if path == "/" {
        ("HTTP/1.1 200 OK", "web/index.html")
    } else {
        ("HTTP/1.1 200 OK", "web/redirect.html")
    };

    if let Ok(contents) = fs::read(filename) {
        let response_header = format!(
            "{}\r\nContent-Length: {}\r\nContent-Type: text/html\r\n\r\n",
            status_line,
            contents.len()
        );
        let _ = stream.write_all(response_header.as_bytes());
        let _ = stream.write_all(&contents);
    }
}
