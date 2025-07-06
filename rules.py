class Rules():
    def __init__(self, board):
        self.board = board

    def check_edges(self):
        for r_index, row in enumerate(self.board.board):
            print('--------------------------------')
            for c_index, cell in enumerate(row):
                if cell:
                    up = self.board.board[r_index - 1][c_index] if r_index - 1 >= 0 else None
                    down = self.board.board[r_index + 1][c_index] if r_index + 1 < len(self.board.board) else None
                    left = self.board.board[r_index][c_index - 1] if c_index - 1 >= 0 else None
                    right = self.board.board[r_index][c_index + 1] if c_index + 1 < len(row) else None

                    print('----')
                    print(f"current: {cell.edges}")
                    if up:
                        print(f"up: {up.edges}")
                    if down:
                        print(f"down: {down.edges}")
                    if left:
                        print(f"left: {left.edges}")
                    if right:
                        print(f"right: {right.edges}")
