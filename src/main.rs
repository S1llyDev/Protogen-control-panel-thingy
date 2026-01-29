use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    // time::Duration,
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
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    eprintln!("New request");
    eprintln!("{}", &http_request[0]);
    eprintln!("{}", &http_request[2]);
    eprintln!("{}", &http_request[http_request.len() -1]);
    eprintln!("{}", &http_request[http_request.len() -2]);
    eprintln!("");

    Command::new("python")
        .arg("py/idunnohowtonamedissorry.py")
        .arg(&http_request[0])
        .spawn()
        .expect("There was an issue with python");

    let request_line = &http_request[0];
    let (status_line, filename) = match &request_line[..] {
        // "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "web/index.html"),
        // "GET /index.css HTTP/1.1" => ("HTTP/1.1 200 OK", "styles/index.css"),
        // "GET /global.css HTTP/1.1" => ("HTTP/1.1 200 OK", "styles/global.css"),

        _ => ("HTTP/1.1 200 OK", "web/success.html"),

        // example of thing if u need to run some code b4 giving file to browser
        // "GET /global.css HTTP/1.1" => { 
        //     *code*
        //     ("HTTP/1.1 200 OK", "styles/global.css")
        // }
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}