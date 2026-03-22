from typing import Optional, Tuple


class StudentPlayer:
    def __init__(self, board_size: int = 6):
        self.n = board_size
        self.board = [[0] * self.n for _ in range(self.n)]
        # flags:1: me; 2: opp
        self.me = 1
        self.opp = 2

    def in_board(self, r, c):
        '''if in the board'''
        return 0 <= r < self.n and 0 <= c < self.n

    def count_dir(self, r, c, dr, dc, who):
        '''return the number of the same flag in one direction(dr, dc)'''
        cnt = 0
        nr, nc = r + dr, c + dc
        while self.in_board(nr, nc) and self.board[nr][nc] == who:
            cnt += 1
            nr += dr
            nc += dc
        return cnt

    def line_len_if_put(self, r, c, who, dr, dc):
        '''return the length of the line if put a flag at (r, c) with direction (dr, dc)'''
        return 1 + self.count_dir(r, c, dr, dc, who) + self.count_dir(r, c, -dr, -dc, who)

    def would_overline(self, r, c, who):
        '''return if >= 5 flags in one direction after puting'''
        for dr, dc in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            if self.line_len_if_put(r, c, who, dr, dc) >= 5:
                return True
        return False

    def would_exact_four(self, r, c, who):
        '''return if = 4'''
        if self.board[r][c] != 0:
            return False
        if self.would_overline(r, c, who):
            return False
        for dr, dc in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            if self.line_len_if_put(r, c, who, dr, dc) == 4:
                return True
        return False

    def is_legal_move(self, r, c, who):
        '''合法移动条件'''
        return self.in_board(r, c) and self.board[r][c] == 0 and (not self.would_overline(r, c, who))

    def candidate_order(self):
        '''所有候选位置排序l1范数'''
        cells = [(r, c) for r in range(self.n) for c in range(self.n)]
        center = (self.n - 1) / 2
        cells.sort(key=lambda x: (abs(x[0] - center) + abs(x[1] - center), x[0], x[1]))
        return cells

    def choose_move(self):
        cells = self.candidate_order()

        # 1) 自己能赢就赢
        for r, c in cells:
            if self.would_exact_four(r, c, self.me):
                return r, c, "I_win"

        # 2) 堵对手立即获胜
        for r, c in cells:
            if self.board[r][c] == 0:
                self.board[r][c] = self.opp
                opp_win = self.would_exact_four(r, c, self.opp) and (not self.would_overline(r, c, self.opp))
                self.board[r][c] = 0
                if opp_win and self.is_legal_move(r, c, self.me):
                    return r, c, "running"

        # 3) 选一个合法且尽量靠中心的位置
        for r, c in cells:
            if self.is_legal_move(r, c, self.me):
                return r, c, "running"

        return 0, 0, "running"

    def step(self, opponent_move: Optional[Tuple[int, int]] = None) -> Tuple[int, int, str]:
        if opponent_move is not None:
            r, c = opponent_move
            if self.in_board(r, c) and self.board[r][c] == 0:
                self.board[r][c] = self.opp

        r, c, status = self.choose_move()
        self.board[r][c] = self.me
        return r, c, status