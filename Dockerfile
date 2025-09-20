# Dockerfile

# Bước 1: Chọn image Python làm nền tảng
FROM python:3.10-slim

# Bước 2: Cài đặt các gói hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Bước 3: Đặt thư mục làm việc trong container
WORKDIR /app

# Bước 4: Sao chép file requirements.txt và cài đặt các thư viện Python
# Tách riêng bước này để tận dụng cache của Docker, giúp build nhanh hơn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bước 5: Sao chép toàn bộ code của bạn (script, model, etc.) vào thư mục làm việc
COPY . .

# Bước 6: Mở cổng 8000 để bên ngoài có thể truy cập vào API
EXPOSE 8000

# Bước 7: Lệnh để khởi chạy web server Uvicorn khi container bắt đầu
# Nó sẽ chạy file `main.py` và đối tượng `app` bên trong file đó
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]