# o-an-quan
## Hướng dẫn cài đặt và chạy game O An Quan
### Môi trờng
- Python 3.8 hoặc cao hơn (recommend 3.11)
- Virtualenv (tùy chọn nhưng khuyến khích)
- Pygame
- PowerShell (Windows) hoặc Terminal (Linux/Mac)
### Cài đặt
# Tạo và kích hoạt virtualenv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Nâng pip và cài pygame
python -m pip install --upgrade pip
pip install pygame

# (Tùy chọn) tạo file requirements
"pygame>=2.1" | Out-File -Encoding utf8 requirements.txt

# Chạy game
python gamegame.py