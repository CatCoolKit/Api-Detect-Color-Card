# 🎯 API Nhận dạng Thẻ Lập Trình Trực Quan

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red.svg)](https://github.com/ultralytics/ultralytics)
[![GitHub](https://img.shields.io/badge/GitHub-CatCoolKit-black.svg)](https://github.com/CatCoolKit)

> **API thông minh sử dụng YOLOv8 để nhận dạng và xử lý các thẻ lệnh lập trình trực quan từ hình ảnh**

## 📋 Tổng quan

Dự án này là một API được xây dựng bằng **FastAPI**, sử dụng mô hình **YOLOv8** để nhận dạng các thẻ lệnh lập trình trực quan từ hình ảnh. API có khả năng xử lý hình ảnh, sắp xếp các thẻ theo đúng thứ tự logic, ghép cặp các thẻ hành động với thẻ số, và trả về một cấu trúc chương trình lồng nhau hoàn chỉnh.

## ✨ Tính năng chính

| Tính năng                  | Mô tả                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 🎯 **Nhận dạng Đối tượng** | Sử dụng YOLOv8 để phát hiện chính xác vị trí và loại thẻ trong ảnh                                                 |
| 🔄 **Sắp xếp Thông minh**  | Tự động phát hiện chiều của ảnh (dù bị lật ngược) và sắp xếp các thẻ theo đúng thứ tự logic từ trên xuống          |
| 🔗 **Ghép cặp Số**         | Ghép các thẻ số (number X) với các thẻ hành động (repeat_start, move_forward, collect) gần nhất một cách chính xác |
| ✅ **Kiểm tra Logic**      | Báo lỗi nếu thiếu thẻ start hoặc nếu số lượng thẻ repeat_start và repeat_end không khớp nhau                       |
| 📊 **Đầu ra có Cấu trúc**  | Trả về kết quả dưới dạng JSON có cấu trúc lồng nhau, thể hiện rõ các khối lệnh lặp                                 |
| 🚀 **API Tinh gọn**        | Lược bỏ các thông tin thừa (confidence, bounding_box) để kết quả trả về gọn gàng và dễ sử dụng                     |

## 🚀 Hướng dẫn cài đặt và chạy

### 📋 Yêu cầu hệ thống

- **Python** 3.8+
- **Pip** (Python package manager)
- **Git** (để clone repository)

### 🔧 Cài đặt

#### 1. Clone repository

```bash
git clone https://github.com/CatCoolKit/Api-Detect-Color-Card.git
cd Api-Detect-Color-Card
```

#### 2. Tạo môi trường ảo (khuyến khích)

```bash
# Trên macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Trên Windows
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

#### 4. Tải model

Đặt file model `my_model.pt` của bạn vào thư mục gốc của dự án.

#### 5. Khởi động server

```bash
uvicorn api:app --reload
```

Server sẽ chạy tại địa chỉ: **http://127.0.0.1:8000**

#### 6. Truy cập tài liệu API

Mở trình duyệt và truy cập [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để xem giao diện Swagger UI và thử nghiệm API.

## 🛠️ Công nghệ sử dụng

| Công nghệ   | Mục đích            | Phiên bản   |
| ----------- | ------------------- | ----------- |
| **FastAPI** | Backend framework   | 0.100+      |
| **Uvicorn** | ASGI server         | Latest      |
| **YOLOv8**  | Object detection    | Ultralytics |
| **OpenCV**  | Image processing    | Latest      |
| **NumPy**   | Numerical computing | Latest      |

## 📁 Cấu trúc dự án

```
Api-Detect-Color-Card/
├── 📄 api.py                 # File API chính
├── 🧠 my_model.pt           # Model YOLOv8 đã train
├── 📋 requirements.txt      # Dependencies
├── 📖 README.md            # Tài liệu dự án
├── 🔍 yolo_detect.py       # Script detection
└── 📁 train/               # Thư mục training
    ├── 📊 results.csv      # Kết quả training
    ├── 📈 *.png           # Biểu đồ metrics
    └── 📁 weights/         # Model weights
        ├── best.pt
        └── last.pt
```

## 🔗 API Endpoints

| Method | Endpoint  | Mô tả                     |
| ------ | --------- | ------------------------- |
| `POST` | `/detect` | Nhận dạng thẻ từ hình ảnh |
| `GET`  | `/health` | Kiểm tra trạng thái API   |
| `GET`  | `/docs`   | Tài liệu API (Swagger UI) |

## 📝 Ví dụ sử dụng

### Gửi request nhận dạng

```bash
curl -X POST "http://127.0.0.1:8000/detect" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Response mẫu

```json
{
  "success": true,
  "program": [
    {
      "type": "start",
      "position": 1
    },
    {
      "type": "repeat_start",
      "number": 3,
      "position": 2,
      "children": [
        {
          "type": "move_forward",
          "position": 3
        }
      ]
    },
    {
      "type": "repeat_end",
      "position": 4
    }
  ]
}
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo một issue hoặc pull request nếu bạn có ý tưởng cải thiện dự án.

## 📄 License

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 👨‍💻 Tác giả

Được phát triển bởi [CatCoolKit](https://github.com/CatCoolKit)

---

<div align="center">
  <p>Được tạo với ❤️ bằng FastAPI và YOLOv8</p>
  <p>⭐ Nếu dự án hữu ích, hãy cho một star nhé!</p>
</div>
