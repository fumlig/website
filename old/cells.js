function init() {
    const rows = 3;
    const cols = 80;

    var cells = [...Array(rows)].map(() => Array(cols));

    for(let r = 0; r < rows; r++) {
        for(let c = 0; c < cols; c++) {
            if(Math.random() >= 0.5) {
                cells[r][c] = ".";
            } else {
                cells[r][c] = " ";
            }
        }
    }

    cells[1].splice(34, 11, "h", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d");

    return cells;
}

function tick(cells, rule) {
    const rows = cells.length;
    const cols = cells[0].length;

    let next = [...Array(rows)].map(() => Array(cols));

    for(let r = 0; r < rows; r++) {
        for(let c = 0; c < cols; c++) {
            next[r][c] = rule(cells, r, c);
        }
    }

    return next;
}

function draw(cells, e) {
    const rows = cells.length;
    const cols = cells[0].length;

    e.textContent = "";
    for(let r = 0; r < rows; r++) {
        for(let c = 0; c < cols; c++) {
            e.textContent += cells[r][c];
        }
        e.textContent += "\n"
    }
}

function conway(cells, r, c) {
    const dead = " ";
    const alive = ".";

    const rows = cells.length;
    const cols = cells[0].length;

    const dr = [-1,-1,-1, 0, 0, 1, 1, 1];
    const dc = [-1, 0, 1,-1, 1,-1, 0, 1];

    let n = 0;

    for(let i = 0; i < 8; i++) {
        const nr = r + dr[i];
        const nc = c + dc[i];

        if(0 <= nr && nr < rows && 0 <= nc && nc < cols) {
            n += cells[nr][nc] != dead;
        }
    }

    if(cells[r][c] != dead && n >= 2 && n <= 3) {
        return cells[r][c];
    } else if(cells[r][c] == dead && n == 3) {
        return alive;
    } else {
        return dead;
    }
}

function snow(cells, r, c) {
    const snow = "*";
    const none = " ";
    
    const rows = cells.length;
    const cols = cells[0].length;

    const nr = (r - 1 + rows) % rows;
    const nc = (c - 1 + cols) % cols;

    return cells[nr][nc];
}

var banner = document.getElementById("banner"); 
var cells = init();

draw(cells, banner);

window.setInterval(() => {
    cells = tick(cells, conway);
    draw(cells, banner);
}, 1000);