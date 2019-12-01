use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn fuel(mass: i32) -> i32 {
  let f = mass / 3 - 2;
  if f > 0 {
    f + fuel(f)
  } else {
    0
  }
}

fn main() -> std::io::Result<()> {
  let mut reader = BufReader::new(File::open("day01.txt")?);

  println!("{}", (reader.lines().map(|l| l.unwrap().parse::<i32>().unwrap() / 3 - 2)).sum::<i32>());
  reader = BufReader::new(File::open("day01.txt")?);
  println!("{}", (reader.lines().map(|l| fuel(l.unwrap().parse::<i32>().unwrap()))).sum::<i32>());
  Ok(())
}
