import unittest
from game import init_board, get_player_pits, valid_moves, refill_if_empty, move, game_over
from constants import N, QUAN_L, QUAN_R, P1_CELLS, P2_CELLS

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Bàn cờ được lưu dưới dạng danh sách các dict chứa sỏi dân và sỏi quan
        self.board = [{"dan": 0, "quan": 0} for _ in range(N)]
        self.board[QUAN_L]["quan"] = 1
        self.board[QUAN_R]["quan"] = 1
        self.scores = [0, 0, 0, 0] # P1 score, P2 score, P1 quan count, P2 quan count

    def test_init_board(self):
        board = init_board()
        self.assertEqual(board[QUAN_L]["quan"], 1)
        self.assertEqual(board[QUAN_R]["quan"], 1)
        for i in P1_CELLS + P2_CELLS:
            self.assertEqual(board[i]["dan"], 5)
            self.assertEqual(board[i]["quan"], 0)

    def test_valid_moves(self):
        board = init_board()
        # Ban đầu tất cả 5 ô đều có sỏi
        self.assertEqual(valid_moves(board, 0), [1, 2, 3, 4, 5])
        # Làm trống một ô
        board[1]["dan"] = 0
        self.assertEqual(valid_moves(board, 0), [2, 3, 4, 5])

    def test_game_over(self):
        self.board[QUAN_L]["quan"] = 0
        self.board[QUAN_R]["quan"] = 0
        self.assertTrue(game_over(self.board))
        
        self.board[QUAN_L]["quan"] = 1
        self.assertFalse(game_over(self.board))

    def test_refill_if_empty_success(self):
        # Điều kiện: Nhà trống, nhưng điểm >= 5 -> Sẽ rải lại mỗi ô 1 viên
        self.scores[0] = 10
        for i in P1_CELLS:
            self.board[i]["dan"] = 0
        
        success = refill_if_empty(self.board, self.scores, 0)
        self.assertTrue(success)
        self.assertEqual(self.scores[0], 5)
        for i in P1_CELLS:
            self.assertEqual(self.board[i]["dan"], 1)

    def test_refill_if_empty_fail(self):
        # Điểm không đủ để rải
        self.scores[0] = 3
        for i in P1_CELLS:
            self.board[i]["dan"] = 0
        
        success = refill_if_empty(self.board, self.scores, 0)
        self.assertFalse(success)

    def test_move_TH1_tiep_tuc_di(self):
        # Trạng thái: Ô 1 có 1 quân, Ô 2 trống, Ô 3 có 2 quân.
        self.board[1]["dan"] = 1
        self.board[2]["dan"] = 0
        self.board[3]["dan"] = 2
        
        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]
        
        self.assertEqual(final_board[1]["dan"], 0)
        self.assertEqual(final_board[2]["dan"], 1)
        self.assertEqual(final_board[3]["dan"], 0)
        self.assertEqual(final_board[4]["dan"], 1)
        self.assertEqual(final_board[5]["dan"], 1)

    def test_move_TH2_an_quan_don(self):
        # Ô 1 có 2 quân. Rải vào 2, 3. Ô 4 trống. Ăn ô 5 có 10 quân.
        self.board[1]["dan"] = 2
        self.board[2]["dan"] = 0
        self.board[3]["dan"] = 0
        self.board[4]["dan"] = 0
        self.board[5]["dan"] = 10
        
        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]

        self.assertEqual(final_scores[0], 10)
        self.assertEqual(final_board[5]["dan"], 0)
        self.assertEqual(final_board[2]["dan"], 1)
        self.assertEqual(final_board[3]["dan"], 1)

    def test_move_TH2_an_lien_hoan(self):
        # Ăn liên tiếp 2 ô (ăn rền)
        self.board[1]["dan"] = 2
        self.board[5]["dan"] = 5
        self.board[6]["quan"] = 0
        self.board[7]["dan"] = 5

        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]

        self.assertEqual(final_scores[0], 10)
        self.assertEqual(final_board[5]["dan"], 0)
        self.assertEqual(final_board[7]["dan"], 0)

    def test_move_TH3_mat_luot_khi_gap_quan(self):
        # Nếu rớt sỏi cuối ở cạnh ô Quan, sẽ không bốc quan đi rải
        self.board[4]["dan"] = 1
        self.board[5]["dan"] = 0
        self.board[6]["quan"] = 1
        self.board[6]["dan"] = 5
        
        frames = move(self.board, self.scores, player=0, cell=4, direction=1)
        final_board, final_scores = frames[-1]
        
        self.assertEqual(final_board[5]["dan"], 1)
        self.assertEqual(final_board[6]["quan"], 1)
        self.assertEqual(final_board[6]["dan"], 5)

if __name__ == '__main__':
    unittest.main()
