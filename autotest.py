import unittest

from gamegame import *

class TestOAnQuan(unittest.TestCase):

    def setUp(self):
        # Hàm này sẽ tự động chạy trước mỗi kịch bản test để reset bàn cờ
        self.board = [0] * N
        self.scores = [0, 0]

    def test_TH1_tiep_tuc_di(self):
        """TH1: Rải xong, ô tiếp theo có quân dân -> Phải bốc lên rải tiếp"""
        # Trạng thái: Ô 1 có 1 quân. Ô 2 trống. Ô 3 có 2 quân.
        self.board[1] = 1
        self.board[2] = 0
        self.board[3] = 2

        # P0 rải từ ô 1 sang phải.
        # Rải viên duy nhất vào ô 2. Ô tiếp theo là 3 (có quân). Phải bốc ô 3 rải tiếp vào 4, 5.
        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]

        # Kiểm tra: Ô 1, 2, 3 phải bằng 0. Ô 4, 5 mỗi ô có 1 quân.
        self.assertEqual(final_board[1], 0)
        self.assertEqual(final_board[2], 1)
        self.assertEqual(final_board[3], 0)
        self.assertEqual(final_board[4], 1)
        self.assertEqual(final_board[5], 1)

    def test_TH2_an_quan_don(self):
        """TH2: Rải xong, ô tiếp theo trống, ô sau nữa có quân -> Ăn quân"""
        # P0 rải ô 1 (có 2 quân).
        self.board[1] = 2
        self.board[2] = 0  # Rải vào đây (1)
        self.board[3] = 0  # Rải vào đây (1) -> Dừng.
        self.board[4] = 0  # Ô tiếp theo trống
        self.board[5] = 10  # Ô bị ăn

        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]

        # Kiểm tra: Điểm P0 = 10. Ô 5 mất sạch quân.
        self.assertEqual(final_scores[0], 10, "Lỗi: P0 không ăn được 10 điểm")
        self.assertEqual(final_board[5], 0, "Lỗi: Ô 5 chưa bị ăn sạch quân")
        self.assertEqual(final_board[2], 1)
        self.assertEqual(final_board[3], 1)

    def test_TH2_an_lien_hoan(self):
        """TH2 (Nâng cao): Ăn chuỗi liên tiếp (Ăn rền)"""
        # Setup thế cờ để ăn liên hoàn 2 nhịp
        self.board[1] = 2
        # Rải 2 quân vào ô 2 và ô 3. Ô 4 trống. Ô 5 có quân -> Ăn ô 5.
        self.board[5] = 5
        # Sau khi ăn ô 5, ô 6 (quan) trống, ô 7 có quân -> Ăn tiếp ô 7.
        self.board[6] = 0
        self.board[7] = 5

        frames = move(self.board, self.scores, player=0, cell=1, direction=1)
        final_board, final_scores = frames[-1]

        # Kiểm tra: Tổng điểm ăn được phải là 10 (ô 5 + ô 7). Các ô bị ăn phải về 0.
        self.assertEqual(final_scores[0], 10, "Lỗi: Không ăn được liên hoàn 10 điểm")
        self.assertEqual(final_board[5], 0)
        self.assertEqual(final_board[7], 0)

    def test_TH3_mat_luot_khi_gap_quan(self):
        """TH3: Nếu liền sau đó là ô quan -> Bị mất lượt (Không được bốc quan)"""
        # P0 rải ô 4 (có 1 quân). Rải vào ô 5. Ô tiếp theo là Quan Phải (Index 6)
        self.board[4] = 1
        self.board[5] = 0
        self.board[6] = 10  # Ô quan đang có quân

        frames = move(self.board, self.scores, player=0, cell=4, direction=1)
        final_board, final_scores = frames[-1]

        # Kiểm tra: Dừng lượt luôn, không được phép bốc 10 quân ở ô 6 đi rải.
        self.assertEqual(final_board[6], 10, "Lỗi: Đã bốc nhầm quân ở ô Quan đi rải")
        self.assertEqual(final_board[5], 1)
        self.assertEqual(final_scores[0], 0)

    def test_TH_dac_biet_het_dan_phai_rai(self):
        """TH Đặc biệt: Hết quân ở 5 ô nhà -> Phải dùng 5 điểm để rải lại"""
        # Setup: P0 không có quân nào ở nhà (Index 1->5). P0 đang có 10 điểm.
        for i in range(1, 6):
            self.board[i] = 0
        self.scores[0] = 10

        # Gọi hàm refill
        success = refill_if_empty(self.board, self.scores, player=0)

        # Kiểm tra: Hàm trả về True. P0 bị trừ 5 điểm. Mỗi ô nhà có 1 quân.
        self.assertTrue(success)
        self.assertEqual(self.scores[0], 5, "Lỗi: Chưa trừ 5 điểm của P0")
        for i in range(1, 6):
            self.assertEqual(self.board[i], 1, f"Lỗi: Ô {i} chưa được rải 1 quân")


if __name__ == '__main__':
    print("Bắt đầu chạy Auto Test Luật Ô Ăn Quan...")
    unittest.main()
