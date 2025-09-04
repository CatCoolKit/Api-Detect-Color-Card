import io
from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
from ultralytics import YOLO
import math
import os
import re

# ==============================================================================
# 1. TẢI MODEL (Chỉ tải một lần khi server khởi động)
# ==============================================================================

# <<< THAY ĐỔI ĐƯỜNG DẪN NÀY cho phù hợp với file model của bạn
MODEL_PATH = "my_model.pt"

# Kiểm tra xem file model có tồn tại không
try:
    model = YOLO(MODEL_PATH, task='detect')
    labels = model.names
    print("Tải model YOLO thành công!")
except Exception as e:
    print(f"Lỗi: Không thể tải model từ đường dẫn: {MODEL_PATH}")
    print(f"Chi tiết lỗi: {e}")
    exit()

# Khởi tạo ứng dụng FastAPI
app = FastAPI(title="YOLO Detection API")


def get_center(bbox: list) -> tuple:
    """Tính toán tọa độ tâm của một bounding box."""
    xmin, ymin, xmax, ymax = bbox
    return ((xmin + xmax) / 2, (ymin + ymax) / 2)

# function test
def sort_detections_path_finding(detections: list) -> list:
    """
    Sắp xếp các vật thể bằng cách tìm đường đi ngắn nhất,
    bắt đầu từ thẻ 'start'.
    """
    if not detections:
        return []

    # 1. Tìm thẻ 'start' để làm điểm bắt đầu
    start_card_index = -1
    for i, d in enumerate(detections):
        if d['class_name'] == 'start':
            start_card_index = i
            break

    # Nếu không tìm thấy thẻ start, không thể sắp xếp -> trả về lỗi hoặc danh sách gốc
    if start_card_index == -1:
        # Tùy chọn: có thể trả về lỗi HTTP ở đây
        print("Cảnh báo: Không tìm thấy thẻ 'start' để bắt đầu sắp xếp.")
        return detections  # Trả về danh sách chưa sắp xếp

    # 2. Khởi tạo danh sách đã sắp xếp và chưa sắp xếp
    sorted_cards = []
    unsorted_cards = detections.copy()  # Tạo một bản sao để làm việc

    # Thêm thẻ 'start' vào danh sách kết quả và xóa khỏi danh sách chưa sắp xếp
    current_card = unsorted_cards.pop(start_card_index)
    sorted_cards.append(current_card)

    # 3. Lặp lại cho đến khi không còn thẻ nào chưa sắp xếp
    while unsorted_cards:
        current_center = get_center(current_card['bounding_box'])

        min_dist = float('inf')
        next_card_index = -1

        # Tìm thẻ gần nhất với thẻ hiện tại
        for i, card in enumerate(unsorted_cards):
            card_center = get_center(card['bounding_box'])
            dist = math.hypot(current_center[0] - card_center[0], current_center[1] - card_center[1])

            if dist < min_dist:
                min_dist = dist
                next_card_index = i

        # Cập nhật thẻ hiện tại là thẻ gần nhất vừa tìm được
        current_card = unsorted_cards.pop(next_card_index)
        sorted_cards.append(current_card)

    return sorted_cards

def sort_detections_top_to_bottom(detections: list) -> list:
    """
    Sắp xếp các vật thể từ trên xuống dưới dựa vào tọa độ y của bounding box.
    """
    # Sắp xếp danh sách detections dựa trên tọa độ y_min (phần tử thứ 2 trong bounding_box)
    return sorted(detections, key=lambda d: d['bounding_box'][1])

def pair_actions_with_numbers(detections: list, threshold_distance: int = 600) -> list:
    """
    Ghép mỗi thẻ số với thẻ hành động hợp lệ gần nhất.
    Cách tiếp cận này ưu tiên tìm "ngôi nhà" tốt nhất cho mỗi thẻ số,
    tránh việc một thẻ hành động ở xa "cướp" mất số của thẻ ở gần.
    """
    ELIGIBLE_ACTIONS = ["repeat_start", "move_forward", "collect"]

    # 1. Phân loại các thẻ để làm việc
    number_cards = [d for d in detections if 'class_name' in d and d['class_name'].startswith('number')]
    action_cards = [d for d in detections if 'class_name' in d and d['class_name'] in ELIGIBLE_ACTIONS]

    # 2. Gán giá trị mặc định cho tất cả các thẻ hành động trước
    for card in action_cards:
        card['value'] = 1

    # 3. Theo dõi các thẻ hành động đã được ghép cặp để đảm bảo mỗi thẻ chỉ nhận một số
    paired_action_cards = set()

    # 4. Với mỗi thẻ số, tìm thẻ hành động tốt nhất (chưa được ghép) cho nó
    for num_card in number_cards:
        num_card_center = get_center(num_card['bounding_box'])

        best_match_action_card = None
        min_dist = float('inf')

        # Tìm trong số các thẻ hành động CHƯA được ghép cặp
        for action_card in action_cards:
            # Dùng id() để so sánh đối tượng duy nhất, tránh nhầm lẫn
            if id(action_card) in paired_action_cards:
                continue  # Bỏ qua thẻ hành động đã được ghép

            action_card_center = get_center(action_card['bounding_box'])
            dist = math.hypot(num_card_center[0] - action_card_center[0], num_card_center[1] - action_card_center[1])

            if dist < min_dist:
                min_dist = dist
                best_match_action_card = action_card

        # 5. Nếu tìm thấy một cặp phù hợp, cập nhật giá trị và đánh dấu là đã ghép
        if best_match_action_card and min_dist < threshold_distance:
            try:
                number_str = re.findall(r'\d+', num_card['class_name'])
                if number_str:
                    # Cập nhật trực tiếp vào thẻ hành động đã tìm thấy
                    best_match_action_card['value'] = int(number_str[0])

                # Đánh dấu thẻ hành động này là đã có cặp
                paired_action_cards.add(id(best_match_action_card))
            except (ValueError, IndexError):
                # Nếu có lỗi, thẻ hành động sẽ giữ giá trị mặc định là 1
                pass

    # 6. Danh sách `detections` gốc đã được cập nhật, chỉ cần trả về nó
    # Không cần sắp xếp lại vì thứ tự không thay đổi.
    return detections

def build_structured_program(simple_detections: list) -> list:
    """
    Xây dựng một cấu trúc chương trình lồng nhau từ một danh sách các lệnh phẳng.
    """
    program = []
    # Stack để theo dõi các khối lệnh lồng nhau, bắt đầu với khối chương trình chính
    stack = [program]

    for detection in simple_detections:
        class_name = detection.get("class_name")

        if class_name == "repeat_start":
            # Tạo một khối lặp mới
            repeat_block = {
                "class_name": "repeat_start",
                "value": detection.get("value", 1),
                "actions": []
            }
            # Thêm khối lặp này vào khối hiện tại
            stack[-1].append(repeat_block)
            # Đẩy danh sách 'actions' của khối mới vào stack để các lệnh tiếp theo được thêm vào đó
            stack.append(repeat_block["actions"])

        elif class_name == "repeat_end":
            # Kết thúc khối lặp hiện tại, quay trở lại khối cha
            if len(stack) > 1:
                stack.pop()

        else:
            # Thêm lệnh thông thường vào khối hiện tại
            stack[-1].append(detection)

    return program


# ==============================================================================
# 2. ĐỊNH NGHĨA API ENDPOINT
# ==============================================================================

@app.post("/detect")
async def detect_objects_in_image(file: UploadFile = File(...),
                                  min_thresh: float = 0.5):
    """
    Endpoint nhận một file ảnh, dò các vật thể bằng YOLO,
    và trả về danh sách các vật thể được phát hiện.
    """
    # ---- Bước 1: Đọc và giải mã ảnh từ file upload ----
    # Đọc dữ liệu dạng bytes từ file
    image_data = await file.read()

    # Chuyển dữ liệu bytes thành mảng NumPy
    nparr = np.frombuffer(image_data, np.uint8)

    # Giải mã mảng NumPy thành ảnh mà OpenCV có thể đọc được
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        raise HTTPException(status_code=400, detail="File ảnh không hợp lệ hoặc bị hỏng.")

    # ---- Bước 2: Chạy dò ảnh trên khung hình ----
    results = model(frame, verbose=False)

    # ---- Bước 3: Xử lý và gom kết quả ----
    detections_list = []
    detections = results[0].boxes

    for i in range(len(detections)):
        conf = detections[i].conf.item()

        # Chỉ lấy các kết quả có độ tin cậy cao hơn ngưỡng
        if conf > min_thresh:
            # Lấy thông tin
            classidx = int(detections[i].cls.item())
            classname = labels[classidx]

            xyxy_tensor = detections[i].xyxy.cpu()
            xyxy = xyxy_tensor.numpy().squeeze().astype(int)

            # Tạo một dictionary cho vật thể này
            detection_info = {
                "class_name": classname,
                "confidence": round(conf, 4),
                "bounding_box": xyxy.tolist()  # Chuyển thành list để tương thích với JSON
            }

            # Thêm vào danh sách kết quả
            detections_list.append(detection_info)

    if not detections_list:
        raise HTTPException(status_code=400, detail="Không tìm thấy thẻ nào trong ảnh.")

    class_names = [d['class_name'] for d in detections_list]

    # Điều kiện 1: Phải có thẻ 'start'
    if 'start' not in class_names:
        raise HTTPException(
            status_code=400,
            detail="Lỗi: Không tìm thấy thẻ 'start'. Vui lòng bắt đầu chương trình bằng thẻ 'start'."
        )

    # Điều kiện 2: Cặp thẻ 'repeat_start' và 'repeat_end' phải khớp nhau
    repeat_start_count = class_names.count('repeat_start')
    repeat_end_count = class_names.count('repeat_end')

    if repeat_start_count != repeat_end_count:
        raise HTTPException(
            status_code=400,
            detail=f"Lỗi: Cặp thẻ lặp không khớp. Tìm thấy {repeat_start_count} thẻ 'repeat_start' nhưng có {repeat_end_count} thẻ 'repeat_end'."
        )

    # ==============================================================================
    # QUY TRÌNH XỬ LÝ
    # ==============================================================================
    # 1. Sắp xếp tất cả các thẻ từ trên xuống
    sorted_detections = sort_detections_top_to_bottom(detections_list)

    # 2. Ghép cặp hành động với số dựa trên danh sách đã sắp xếp
    processed_detections = pair_actions_with_numbers(sorted_detections)

    # 3. Lược bỏ các trường không cần thiết để chuẩn bị xây dựng cấu trúc
    final_detections = [d for d in processed_detections if not d['class_name'].strip().startswith('number')]

    simple_detections = []
    for detection in final_detections:
        new_detection = {"class_name": detection["class_name"]}
        if "value" in detection:
            new_detection["value"] = detection["value"]
        simple_detections.append(new_detection)

    # 4. Xây dựng cấu trúc chương trình lồng nhau
    structured_program = build_structured_program(simple_detections)

    # test = sort_detections_path_finding(detections_list)

    return {"detections": structured_program}


@app.get("/")
def root():
    return {"message": "Chào mừng đến với YOLO Detection API. Hãy truy cập /docs để thử nghiệm."}