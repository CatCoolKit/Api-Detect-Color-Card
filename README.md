API Nhận dạng Thẻ lập trình 可视化 (Visual Programming Card Recognition API)

Dự án này là một API được xây dựng bằng FastAPI, sử dụng mô hình YOLOv8 để nhận dạng các thẻ lệnh lập trình 可视化 từ hình ảnh. API có khả năng xử lý hình ảnh, sắp xếp các thẻ theo đúng thứ tự logic, ghép cặp các thẻ hành động với thẻ số, và trả về một cấu trúc chương trình lồng nhau hoàn chỉnh.



<!-- Bạn nên thay link ảnh này bằng một ảnh ví dụ của dự án -->



✨ Tính năng chính

Nhận dạng Đối tượng: Sử dụng YOLOv8 để phát hiện chính xác vị trí và loại thẻ trong ảnh.



Sắp xếp Thông minh: Tự động phát hiện chiều của ảnh (dù bị lật ngược) và sắp xếp các thẻ theo đúng thứ tự logic từ trên xuống.



Ghép cặp Số: Ghép các thẻ số (number X) với các thẻ hành động (repeat\_start, move\_forward, collect) gần nhất một cách chính xác.



Kiểm tra Logic: Báo lỗi nếu thiếu thẻ start hoặc nếu số lượng thẻ repeat\_start và repeat\_end không khớp nhau.



Đầu ra có Cấu trúc: Trả về kết quả dưới dạng JSON có cấu trúc lồng nhau, thể hiện rõ các khối lệnh lặp.



API Tinh gọn: Lược bỏ các thông tin thừa (confidence, bounding\_box) để kết quả trả về gọn gàng và dễ sử dụng.



🚀 Hướng dẫn chạy trên máy cá nhân (Local)

Yêu cầu:



Python 3.8+



Pip



Các bước cài đặt:



Clone repository:



git clone \[https://github.com/ten-cua-ban/ten-repository.git](https://github.com/ten-cua-ban/ten-repository.git)

cd ten-repository



Tạo môi trường ảo (khuyến khích):



\# Trên macOS/Linux

python3 -m venv venv

source venv/bin/activate



\# Trên Windows

python -m venv venv

.\\venv\\Scripts\\activate



Cài đặt các thư viện cần thiết:



pip install -r requirements.txt



Tải model:

Đặt file model my\_model.pt của bạn vào thư mục gốc của dự án.



Khởi động server:

Nếu file chính của bạn là api.py:



uvicorn api:app --reload



Server sẽ chạy tại địa chỉ http://127.0.0.1:8000.



Truy cập tài liệu API:

Mở trình duyệt và truy cập http://127.0.0.1:8000/docs để xem giao diện Swagger UI và thử nghiệm API.



🛠️ Công nghệ sử dụng

Backend: FastAPI



Server: Uvicorn



Nhận dạng đối tượng: YOLOv8 (Ultralytics)



Xử lý ảnh: OpenCV, NumPy

