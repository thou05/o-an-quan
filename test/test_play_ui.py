import unittest
import sys
from unittest.mock import MagicMock

# Mock pygame để có thể load file play_ui.py mà không lỗi (khi chạy không có cửa sổ console hoặc giao diện màn hình)
sys.modules['pygame'] = MagicMock()

# Vì play_ui import pygame từ mọi file nên ta mock trước
from play_ui import format_time

class TestPlayUI(unittest.TestCase):
    def test_format_time(self):
        # Kiểm tra logic chuyển số giây thành format mm:ss
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(59), "00:59")
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(125), "02:05")
        self.assertEqual(format_time(3600), "60:00")

if __name__ == '__main__':
    unittest.main()
