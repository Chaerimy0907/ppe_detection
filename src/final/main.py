import cv2
import csv
import os
from datetime import datetime, timedelta
from ultralytics import YOLO

# ========================
# Configuration Parameters
# ========================
class Config:
    MODEL_PATH = '../../models/best.pt'     # TOLO 모델 경로
    CONF_THRESHOLD = 0.4                    # 정확도(신뢰도) 40% 이상만 인식에 사용
    TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX    # 텍스트 출력할 때 사용할 글씨체
    TEXT_COLOR = (255, 255, 255)            # 흰색 글씨
    FRAME_DELAY = 5                         # 프레임 간 대기 시간 (ms)
    CSV_PATH = './ppe_log.csv'              # 통계 로그 저장 경로

    # PPE 착용 상태에 따른 박스 색상
    LABEL_COLORS = {
        'perfect': (0, 255, 0),      # PPE 완벽 착용 : 초록
        'imperfect': (0, 0, 255),    # PPE 미착용 또는 불완전 : 빨강
    }

    # 화면 상 통계 텍스트 위치 좌표
    TEXT_POS = {
        'total': (30, 40),      # 총 인원 수
        'perfect': (30, 80),    # PPE 완벽 착용 인원 수
        'ratio': (30, 120),     # 착용 비율(%)
        'alert': (30, 160),     # 경고 문구
    }


# ========================
# Utility Functions
# ========================
def get_box_center(bbox):
    """박스 중심 좌표 계산 (x1, y1, x2, y2 → 중심점)"""
    x1, y1, x2, y2 = bbox
    return (x1 + x2) // 2, (y1 + y2) // 2

def center_inside(ppe_box, person_box):
    """PPE의 중심점이 사람 박스 안에 들어있으면 착용한 것으로 판단
    """
    cx, cy = get_box_center(ppe_box)
    x1, y1, x2, y2 = person_box
    return x1 <= cx <= x2 and y1 <= cy <= y2

def draw_text(frame, text, position, color, size=0.8, thickness=2):
    """프레임에 텍스트 렌더링"""
    cv2.putText(frame, text, position, Config.TEXT_FONT, size, color, thickness)

def draw_box(frame, bbox, color):
    """
    객체를 사각형 박스로 그리기
    PPE 착용 여부에 따라 색상이 달라짐
    """
    x1, y1, x2, y2 = bbox
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

def save_csv(path, timestamp, avg_total, avg_ratio):
    """
    평균 인원수 및 착용률을 CSV 파일에 저장
    파일이 없으면 자동 생성
    """
    row = [timestamp.strftime('%Y-%m-%d %H:%M:%S'), avg_total, round(avg_ratio, 1)]
    header = ['Timestamp', 'Average Total People', 'Average Perfect Ratio (%)']
    file_exists = os.path.isfile(path)

    with open(path, mode='a' if file_exists else 'w', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)


# ========================
# Main Detection Pipeline
# ========================
def detect_ppe(video_path):
    """
    비디오 프레임에서 사람 및 PPE를 감지하고,
    PPE 착용 상태를 판단하여 시각화 + 통계 로그 저장
    """
    model = YOLO(Config.MODEL_PATH) # 사용할 모델 불러오기
    cap = cv2.VideoCapture(video_path)  # 비디오 파일 열기

    if not cap.isOpened():
        print("동영상 읽기 실패")
        return
    
    # 누적 통계 관련 변수 초기화
    total_history = []      # 누적 인원 수 저장
    perfect_history = []    # 누적 착용자 수 저장
    last_saved_time = datetime.now()
    
    # 프레임 반복 처리
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 리사이즈 (성능 개선)
        frame = cv2.resize(frame, (640, 360))

        # YOLO 감지 수행 (verbose=False로 로그 억제)
        results = model(frame, verbose=False)
        detection = results[0]

        # 감지된 객체별 박스 저장용 리스트
        person_boxes, hardhat_boxes, vest_boxes = [], [], []

        # 감지된 객체 분류
        for box in detection.boxes:
            cls_id = int(box.cls[0])        # 클래스 ID
            confidence = float(box.conf[0])       # 신뢰도
            label = model.names[cls_id]     # 클래스 이름

            if confidence < Config.CONF_THRESHOLD:
                continue    # 신뢰도 낮으면 무시함

            # 좌표 값 가져오기
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bbox = (x1, y1, x2, y2)

            # 클래스별로 리스트에 저장
            if label == 'Person':
                person_boxes.append(bbox)
            elif label == 'Hardhat':
                hardhat_boxes.append(bbox)
            elif label == 'Safety Vest':
                vest_boxes.append(bbox)

        # PPE 착용 판별
        perfect_count = 0   # 완벽 착용자 수
        for person_box in person_boxes:
            # 사람 박스 안에 안전모와 안전조끼가 있는지 확인
            has_hat = any(center_inside(h, person_box) for h in hardhat_boxes)
            has_vest = any(center_inside(v, person_box) for v in vest_boxes)

            if has_hat and has_vest:
                perfect_count += 1
                draw_box(frame, person_box, Config.LABEL_COLORS['perfect'])
            else:
                draw_box(frame, person_box, Config.LABEL_COLORS['imperfect'])
            
        # 통계 수치 계산
        total_count = len(person_boxes)
        ratio = (perfect_count / total_count) * 100 if total_count else 0

        # 영상에 통계 표시 (총 인원, 완벽 착용자 수, 비율)
        draw_text(frame, f'Total: {total_count}', Config.TEXT_POS['total'], Config.TEXT_COLOR)
        draw_text(frame, f'Perfect: {perfect_count}', Config.TEXT_POS['perfect'], Config.LABEL_COLORS['perfect'])
        draw_text(frame, f'Ratio: {ratio:.1f}%', Config.TEXT_POS['ratio'], (0, 255, 255))

        # 경고 문구 출력 (2명 이상 미착용 시)
        if total_count - perfect_count >= 2:
            draw_text(frame, 'No Wearing', Config.TEXT_POS['alert'], Config.LABEL_COLORS['imperfect'], 0.9, 3)

        # 누적 통계 저장
        total_history.append(total_count)
        perfect_history.append(perfect_count)

        # 10초마다 통계 저장 (테스트용, 실사용시 timedelta(hours=1) 로 변경하여 사용)
        now = datetime.now()
        if now - last_saved_time >= timedelta(seconds=10):
            if total_history:
                avg_total = round(sum(total_history) / len(total_history))
                avg_perfect = round(sum(perfect_history) / len(perfect_history))
                avg_ratio = (avg_perfect / avg_total) * 100 if avg_total > 0 else 0

                save_csv(Config.CSV_PATH, now, avg_total, avg_ratio)

                # 누적값 초기화
                last_saved_time = now
                total_history.clear()
                perfect_history.clear()

        # 결과 화면 출력
        cv2.imshow("PPE Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료 시 마지막 통계 저장
    if total_history:
        now = datetime.now()
        avg_total = round(sum(total_history) / len(total_history))
        avg_perfect = round(sum(perfect_history) / len(perfect_history))
        avg_ratio = (avg_perfect / avg_total) * 100 if avg_total else 0
        save_csv(Config.CSV_PATH, now, avg_total, avg_ratio)

    cap.release()
    cv2.destroyAllWindows()


# 실행 부분
if __name__ == "__main__":
    # 감지할 비디오 파일 경로 지정
    detect_ppe('../../img/hardhat1.mp4')