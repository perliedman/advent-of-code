use std::env;

fn count_safe(row: &str) -> u32 {
	let mut n_safe = 0;
	for c in row.chars() {
		n_safe += match c {
			'.' => 1,
			_ =>0
		};
	}

	return n_safe;
}

fn group_to_tile(g: &str) -> char {	
	let r = match g.as_ref() {
		"^^." | ".^^" | "^.." | "..^" => '^',
		_ => '.'
	};
//	println!("{} => {}", g, r);
	return r;
}

fn next_row(row: &str) -> String {
	let mut s = ".".to_string();
	let mut result = "".to_string();
	let mut chars = row.chars();
	s.push(match chars.next() { Some(c) => c, _ => panic!("No chars in row")});

	for c in chars {
		s.push(c);
		result.push(group_to_tile(&s));
		s = s[1..3].to_string();
	}

	s.push('.');
	result.push(group_to_tile(&s));

	return result;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut row = args[1].clone();
    let mut n_safe = 0;

    for _ in 1..400001 {
//    	println!("{}", row);
    	n_safe += count_safe(&row);
    	row = next_row(&row);
    }

    println!("{}", n_safe);
}
