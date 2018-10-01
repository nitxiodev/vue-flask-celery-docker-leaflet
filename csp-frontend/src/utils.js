const SUDOKU_GRID = [...new Array(81).keys()];
const random_between = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1) + min);
};
const parse = sudoku => {
  return sudoku.split("").map(Number);
};
const download = sudoku => {
  return sudoku.map(Number).join("");
};
const in_range = (min, max, value) => {
  return min <= value && value <= max;
};
const level = sudoku => {
  let filled_cells = sudoku.reduce(function(n, val) {
    return n + (val > 0);
  }, 0);

  let cur_level;

  if (in_range(8, 16, filled_cells)) {
    cur_level = 6;
  } else if (in_range(17, 27, filled_cells)) {
    cur_level = 5;
  } else if (in_range(28, 31, filled_cells)) {
    cur_level = 4;
  } else if (in_range(32, 35, filled_cells)) {
    cur_level = 3;
  } else if (in_range(36, 46, filled_cells)) {
    cur_level = 2;
  } else {
    cur_level = 1;
  }

  return cur_level;
};
const colors = [
  "rgba(7, 0, 145, 0.65)",
  "rgba(6, 145, 0, 0.65)",
  "rgba(145, 21, 2, 0.65)",
  "rgba(137, 140, 145, 0.65)",
  "rgba(145, 0, 142, 0.65)",
  "rgba(0, 140, 145, 0.65)",
  "rgba(145, 140, 0, 0.65)"
];

const getColor = function(d) {
  let cur_color;
  switch (d) {
    case 1:
      cur_color = colors[0];
      break;
    case 2:
      cur_color = colors[1];
      break;
    case 3:
      cur_color = colors[2];
      break;
    case 4:
      cur_color = colors[3];
      break;
    case 5:
      cur_color = colors[4];
      break;
    case 6:
      cur_color = colors[5];
      break;
    default:
      cur_color = colors[6];
      break;
  }
  return cur_color;
};

export { random_between, SUDOKU_GRID, parse, download, level, getColor };
