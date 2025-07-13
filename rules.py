class Rules():
    def __init__(self, board):
        self.board = board
        self.matches = {}

    def match_edges(self):
        matches = {}
        for r_index, row in enumerate(self.board.board):
            for c_index, cell in enumerate(row):
                if cell:
                    matches[cell] = {}
                    up = self.board.board[r_index - 1][c_index] if r_index - 1 >= 0 else None
                    down = self.board.board[r_index + 1][c_index] if r_index + 1 < len(self.board.board) else None
                    left = self.board.board[r_index][c_index - 1] if c_index - 1 >= 0 else None
                    right = self.board.board[r_index][c_index + 1] if c_index + 1 < len(row) else None

                    if up and cell.edges[0] == up.edges[2]:
                        matches[cell]["up"] = up
                    if down and cell.edges[2] == down.edges[0]:
                        matches[cell]["down"] = down
                    if left and cell.edges[3] == left.edges[1]:
                        matches[cell]["left"] = left
                    if right and cell.edges[1] == right.edges[3]:
                        matches[cell]["right"] = right

        self.matches = matches
