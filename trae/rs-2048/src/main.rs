use rand::Rng;
use std::io::{self, Write};
use std::process;

const SIZE: usize = 4;

struct Board {
    grid: [[u32; SIZE]; SIZE],
    score: u32,
}

impl Board {
    fn new() -> Self {
        let mut board = Board {
            grid: [[0; SIZE]; SIZE],
            score: 0,
        };
        board.add_random_tile();
        board.add_random_tile();
        board
    }

    fn add_random_tile(&mut self) {
        let mut rng = rand::thread_rng();
        let mut empty_cells = Vec::new();

        for i in 0..SIZE {
            for j in 0..SIZE {
                if self.grid[i][j] == 0 {
                    empty_cells.push((i, j));
                }
            }
        }

        if !empty_cells.is_empty() {
            let (i, j) = empty_cells[rng.gen_range(0..empty_cells.len())];
            self.grid[i][j] = if rng.gen_range(0..10) < 9 { 2 } else { 4 };
        }
    }

    fn print(&self) {
        println!("Score: {}", self.score);
        for row in &self.grid {
            println!("+----+----+----+----+");
            print!("|");
            for &cell in row {
                if cell == 0 {
                    print!("    |");
                } else {
                    print!("{:4}|", cell);
                }
            }
            println!();
        }
        println!("+----+----+----+----+");
    }

    fn move_left(&mut self) -> bool {
        let mut moved = false;
        for i in 0..SIZE {
            let (new_row, score_change, row_moved) = Self::merge_row(self.grid[i]);
            if row_moved {
                self.grid[i] = new_row;
                self.score += score_change;
                moved = true;
            }
        }
        moved
    }

    fn merge_row(row: [u32; SIZE]) -> ([u32; SIZE], u32, bool) {
        let mut new_row = [0; SIZE];
        let mut index: usize = 0;
        let mut score_change = 0;
        let mut moved = false;
        let mut prev: Option<u32> = None;

        for &cell in &row {
            if cell != 0 {
                if let Some(val) = prev {
                    if val == cell {
                        new_row[index] = val * 2;
                        score_change += val * 2;
                        index += 1;
                        prev = None;
                        moved = true;
                    } else {
                        new_row[index] = val;
                        index += 1;
                        prev = Some(cell);
                        if val != cell {
                            moved = true;
                        }
                    }
                } else {
                    prev = Some(cell);
                }
            }
        }

        if let Some(val) = prev {
            new_row[index] = val;
            if index != row.iter().position(|&x| x == val).unwrap() {
                moved = true;
            }
        }

        (new_row, score_change, moved)
    }

    fn rotate(&mut self) {
        let mut new_grid = [[0; SIZE]; SIZE];
        for i in 0..SIZE {
            for j in 0..SIZE {
                new_grid[i][j] = self.grid[SIZE - j - 1][i];
            }
        }
        self.grid = new_grid;
    }

    fn move_right(&mut self) -> bool {
        self.rotate();
        self.rotate();
        let moved = self.move_left();
        self.rotate();
        self.rotate();
        moved
    }

    fn move_up(&mut self) -> bool {
        self.rotate();
        self.rotate();
        self.rotate();
        let moved = self.move_left();
        self.rotate();
        moved
    }

    fn move_down(&mut self) -> bool {
        self.rotate();
        let moved = self.move_left();
        self.rotate();
        self.rotate();
        self.rotate();
        moved
    }

    fn is_game_over(&self) -> bool {
        for i in 0..SIZE {
            for j in 0..SIZE {
                if self.grid[i][j] == 0 {
                    return false;
                }
                if j < SIZE - 1 && self.grid[i][j] == self.grid[i][j + 1] {
                    return false;
                }
                if i < SIZE - 1 && self.grid[i][j] == self.grid[i + 1][j] {
                    return false;
                }
            }
        }
        true
    }
}

fn main() {
    let mut board = Board::new();
    loop {
        print!("\x1B[2J\x1B[1;1H"); // 清屏
        board.print();

        if board.is_game_over() {
            println!("Game Over! Final Score: {}", board.score);
            break;
        }

        println!("Use WASD or arrow keys to move (Q to quit)");
        print!("> ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        let moved = match input.trim().to_lowercase().as_str() {
            "w" | "up" => board.move_up(),
            "a" | "left" => board.move_left(),
            "s" | "down" => board.move_down(),
            "d" | "right" => board.move_right(),
            "q" => {
                println!("Quitting game...");
                process::exit(0);
            }
            _ => {
                println!("Invalid input!");
                false
            }
        };

        if moved {
            board.add_random_tile();
        }
    }
}
