use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let host: &str = match args.get(1) {
        Some(h) => h,
        None => {
            eprintln!("Usage: {} <url> [port] [max_sockets]", args[0]);
            std::process::exit(1);
        }
    };
    let port: u16 = args
        .get(2)
        .map(|p| p.parse().expect("port must be a number 0-65535"))
        .unwrap_or(80);
    let max_sockets: usize = args
        .get(3)
        .map(|m| m.parse().expect("max_sockets must be a non-negative integer"))
        .unwrap_or(150);
    println!("host: {host}, port: {port}, max_sockets: {max_sockets}");
}