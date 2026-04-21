import unittest
from ai import evaluate, get_best_move
from game import move
from constants import N, QUAN_L, QUAN_R

class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = [{"dan": 0, "quan": 0} for _ in range(N)]
        self.board[QUAN_L]["quan"] = 1
        self.board[QUAN_R]["quan"] = 1
        self.scores = [0, 0, 0, 0]
        
    def test_evaluate_basic(self):
        # Tình trạng: AI (Player 1) có nhiều điểm hơn
        self.scores[1] = 20 # Điểm AI
        self.scores[0] = 5  # Điểm người chơi thực
        
        score = evaluate(self.board, self.scores, player_ai=1)
        self.assertTrue(score > 0, "Điểm phải dương khi AI hơn điểm")
        
        # Tình trạng: Người chơi thực có nhiều điểm hơn
        self.scores[1] = 0
        self.scores[0] = 50
        score2 = evaluate(self.board, self.scores, player_ai=1)
        self.assertTrue(score2 < 0, "Điểm phải âm khi AI thua điểm")

    def test_get_best_move_no_moves(self):
        # Khi không còn nước đi hợp lệ
        best_move = get_best_move(self.board, self.scores, player_ai=1, move_func=move)
        self.assertIsNone(best_move)

    def test_get_best_move_returns_move(self):
        # AI có thể đi một vài nước
        self.board[7]["dan"] = 5
        self.board[8]["dan"] = 5
        best_move = get_best_move(self.board, self.scores, player_ai=1, move_func=move)
        
        self.assertIsNotNone(best_move)
        self.assertIn(best_move[0], [7, 8])
        self.assertIn(best_move[1], [1, -1])

if __name__ == '__main__':
    unittest.main()
