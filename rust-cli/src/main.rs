use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: rust-cli <config-file>");
        process::exit(1);
    }

    let filename = &args[1];
    let contents = match fs::read_to_string(filename) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Error reading {}: {}", filename, e);
            process::exit(1);
        }
    };

    match rust_cli::parse_config(&contents) {
        Ok(config) => {
            println!("Loaded {} config entries:", config.len());
            for (key, value) in &config {
                println!("  {} = {}", key, rust_cli::truncate(value, 40));
            }
        }
        Err(e) => {
            eprintln!("Config parse error: {}", e);
            process::exit(1);
        }
    }
}
