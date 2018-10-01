const SUDOKU_GRID = require("./utils").SUDOKU_GRID;
let random_between = require("./utils").random_between;
let parse = require("./utils").parse;
let download = require("./utils").download;
let getLevel = require("./utils").level;

/**
 * https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
 */
const fisher_yates = numbers => {
  for (let i = numbers.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * i);

    // swap
    let temp = numbers[j];
    numbers[j] = numbers[i];
    numbers[i] = temp;
  }

  return numbers;
};

/**
 * Based on https://gamedev.stackexchange.com/questions/56149/how-can-i-generate-sudoku-puzzles
 */
const generator = difficulty => {
  let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  let shuffled_numbers = fisher_yates(numbers);
  let sudoku_grid = [shuffled_numbers];
  let slice_data;

  for (let i = 1; i < 9; i++) {
    slice_data = 3;
    if (i % 3 == 0) {
      slice_data = 1;
    }
    shuffled_numbers = shuffled_numbers
      .slice(slice_data)
      .concat(shuffled_numbers.slice(0, slice_data));
    sudoku_grid.push(shuffled_numbers);
  }
  let sudoku = [].concat.apply([], sudoku_grid); // flatten sudoku
  levels(difficulty, sudoku);

  return sudoku;
};

/**
 * Extremely easy (1): > 46 cells.
 * Easy (2): 36-46 cells.
 * Medium (3): 32-35 cells.
 * Hard (4): 28-31 cells.
 * Evil (5): 17-27 cells.
 * Insane (6): 13-16 cells.
 */
const levels = (level, sudoku) => {
  let number_of_cells;
  switch (level) {
    case 1:
      number_of_cells = random_between(47, 80);
      break;
    case 2:
      number_of_cells = random_between(36, 46);
      break;
    case 3:
      number_of_cells = random_between(32, 35);
      break;
    case 4:
      number_of_cells = random_between(28, 31);
      break;
    case 5:
      number_of_cells = random_between(17, 27);
      break;
    case 6:
      number_of_cells = random_between(8, 16);
      break;
    default:
      number_of_cells = 75;
      break;
  }
  let deleted_cells = fisher_yates(SUDOKU_GRID).slice(0, 81 - number_of_cells);
  for (let i = 0; i < deleted_cells.length; i++) {
    sudoku[deleted_cells[i]] = 0;
  }
};

/**
 * Convert sudoku grid into sudoku string
 */
const download_sdk = sudoku => {
  return download(sudoku);
};

const upload = sudoku => {
  return parse(sudoku);
};

module.exports = {
  shuffle: fisher_yates,
  gen: generator,
  download_sudoku: download_sdk,
  parse: upload,
  level: getLevel
};
