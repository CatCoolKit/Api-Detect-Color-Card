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
├── 📁 images/              # Thư mục ảnh mẫu
│   ├── 🎯 sample_cards.jpg # Ảnh mẫu các thẻ lệnh
│   ├── 🔄 example_1.jpg    # Ví dụ 1: Thẻ đơn giản
│   ├── 🔄 example_2.jpg    # Ví dụ 2: Thẻ có vòng lặp
│   └── 🔄 example_3.jpg    # Ví dụ 3: Thẻ phức tạp
└── 📁 train/               # Thư mục training
    ├── 📊 results.csv      # Kết quả training
    ├── 📈 *.png           # Biểu đồ metrics
    └── 📁 weights/         # Model weights
        ├── best.pt
        └── last.pt
```

## 🖼️ Ảnh mẫu

### Các loại thẻ được hỗ trợ

Dự án hỗ trợ nhận dạng **17 loại thẻ** lập trình trực quan sau:

#### Bảng tổng quan

| Loại thẻ            | Mô tả                    | Ví dụ          |
| ------------------- | ------------------------ | -------------- |
| 🚀 **start**        | Thẻ bắt đầu chương trình | `start`        |
| 🔢 **number 1-9**   | Thẻ số (1, 2, 3, ..., 9) | `number 3`     |
| 🔄 **repeat_start** | Bắt đầu vòng lặp         | `repeat_start` |
| 🔚 **repeat_end**   | Kết thúc vòng lặp        | `repeat_end`   |
| ⬆️ **move_forward** | Di chuyển tiến           | `move_forward` |
| ⬅️ **turn_left**    | Rẽ trái                  | `turn_left`    |
| ➡️ **turn_right**   | Rẽ phải                  | `turn_right`   |
| 🔄 **turn_back**    | Quay lại                 | `turn_back`    |
| 📦 **collect**      | Thu thập                 | `collect`      |

#### Danh sách đầy đủ các thẻ

<details>
<summary>📋 Xem danh sách đầy đủ 17 loại thẻ</summary>

| STT | Tên thẻ        | Mô tả                    | Loại     |
| --- | -------------- | ------------------------ | -------- |
| 1   | `start`        | Thẻ bắt đầu chương trình | Control  |
| 2   | `collect`      | Thu thập vật phẩm        | Action   |
| 3   | `move_forward` | Di chuyển tiến           | Movement |
| 4   | `number 1`     | Thẻ số 1                 | Number   |
| 5   | `number 2`     | Thẻ số 2                 | Number   |
| 6   | `number 3`     | Thẻ số 3                 | Number   |
| 7   | `number 4`     | Thẻ số 4                 | Number   |
| 8   | `number 5`     | Thẻ số 5                 | Number   |
| 9   | `number 6`     | Thẻ số 6                 | Number   |
| 10  | `number 7`     | Thẻ số 7                 | Number   |
| 11  | `number 8`     | Thẻ số 8                 | Number   |
| 12  | `number 9`     | Thẻ số 9                 | Number   |
| 13  | `repeat_end`   | Kết thúc vòng lặp        | Control  |
| 14  | `repeat_start` | Bắt đầu vòng lặp         | Control  |
| 15  | `turn_back`    | Quay lại                 | Movement |
| 16  | `turn_left`    | Rẽ trái                  | Movement |
| 17  | `turn_right`   | Rẽ phải                  | Movement |

</details>

## 🔗 API Endpoints

| Method | Endpoint | Mô tả                     |
| ------ | -------- | ------------------------- |
| `GET`  | `/docs`  | Tài liệu API (Swagger UI) |

## 📝 Ví dụ sử dụng

### Gửi request nhận dạng

```bash
curl -X POST "http://127.0.0.1:8000/docs" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Response mẫu

```json
{
  "detections": [
    {
      "class_name": "start"
    },
    {
      "class_name": "repeat_start",
      "value": 5,
      "actions": [
        {
          "class_name": "move_forward",
          "value": 8
        }
      ]
    },
    {
      "class_name": "collect",
      "value": 2
    },
    {
      "class_name": "turn_left"
    },
    {
      "class_name": "turn_right"
    },
    {
      "class_name": "turn_back"
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
