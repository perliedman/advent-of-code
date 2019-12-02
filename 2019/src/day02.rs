use std::fs;

fn run(contents: &str, noun: i32, verb: i32) -> i32 {
  let mut memory: Vec<i32> = contents.split(',').map(|x| x.parse::<i32>().unwrap()).collect();
  let mut pc = 0;

  memory[1] = noun;
  memory[2] = verb;

  loop {
    let opcode = memory[pc];
    let a = memory[pc + 1] as usize;
    let b = memory[pc + 2] as usize;
    let dest = memory[pc + 3] as usize; 

    println!("{} {} {} {}", opcode, a, b, dest);

    match opcode {
      1 => {
        memory[dest] = memory[a] + memory[b];
      }
      2 => {
        memory[dest] = memory[a] * memory[b];
      }
      99 => {
        return memory[0];
      }
      _ => {
        panic!("Unexpected opcode {}", opcode);
      }
    }

    pc = pc + 4
  }
}

fn main() -> std::io::Result<()> {
  let contents = fs::read_to_string("day02.txt").unwrap();

  println!("{}", run(&contents, 12, 2));

  for i in 0..100 {
    for j in 0..100 {
      if run(&contents, i, j) == 19690720 {
        println!("{}, {} => {}", i, j, 100 * i + j);
        return Ok(())
      }
    }
  }

  Ok(())
}
