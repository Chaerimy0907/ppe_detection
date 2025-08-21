"""
1시간 마다 통계 CSV 저장 기능
"""

# YOLO 모델을 불러오기 위한 라이브러리
from ultralytics import YOLO
# 비디오 처리와 화면 출력 등을 위한 OpenCV 라이브러리
import cv2
import csv
from datetime import datetime, timedelta

# 설정값
class Config:
    MODEL_PATH = '../../models/best.pt'  # 사용할 YOLO 모델 파일 이름
    CONF_THRESHOLD = 0.4    # 정확도(신뢰도) 40% 이상만 인식에 사용
    TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX    # 텍스트 출력할 때 사용할 글씨체
    TEXT_COLOR = (255, 255, 255)            # 흰색 글씨
    FRAME_DELAY = 5                         # 프레임 간 간격

    # 상자 색상 설정(각 사람마다 제대로 착용했는지에 따라 색 다르게)
    LABEL_COLORS = {
        'perfect': (0, 255, 0),     # 초록 : 완벽 착용
        'imperfect': (0, 0, 255),    # 빨강 : 미착용
    }

    # 글자 위치 (영상에서 글자가 어디에 나올지 좌표 설정)
    TEXT_POS = {
        'total': (30, 40),      # 총 인원 수 표시 위치
        'perfect': (30, 80),    # PPE 완벽 착용 인원 수 표시 위치
        'ratio': (30, 120),     # 착용 비율(%) 표시 위치
        'alert': (30, 160),     # 경고 메시지 위치
    }

# 유틸리티 함수들

# def is_inside(inner_box, outer_box):
#     """
#     작은 박스(inner)가 큰 박스(outer) 안에 완전히 들어가 있는지 확인하는 함수
#     ex) 안전모 박스(inner)가 사람 박스(outer) 안에 들어가 있으면
#     안전모를 착용했다고 판단
#     """
#     ix1, iy1, ix2, iy2 = inner_box  # 안쪽 박스 좌표
#     ox1, oy1, ox2, oy2 = outer_box  # 바깥 박스 좌표
#     return ix1 >= ox1 and iy1 >= oy1 and ix2 <= ox2 and iy2 <= oy2

def box_center(box):
    """박스 중심 좌표 계산 (x1, y1, x2, y2 -> 중심점)"""
    x1, y1, x2, y2 = box
    return (x1 + x2) // 2, (y1 + y2) // 2

def center_inside(ppe_box, person_box):
    """PPE의 중심점이 사람 박스 안에 들어있으면 착용한 걸로 판단
    (기존의 def is_inside(inner_box, outer_box) 보다 더 빠르고 유연한 방식)
    """
    cx, cy = box_center(ppe_box)
    x1, y1, x2, y2 = person_box
    return x1 <= cx <= x2 and y1 <= cy <= y2

def draw_text(frame, text, position, color, size=0.8, thickness=2):
    """화면에 글씨를 출력해주는 함수"""
    cv2.putText(frame, text, position, Config.TEXT_FONT, size, color, thickness)

def draw_person_box(frame, box, color):
    """
    사람을 네모 박스로 표시해주는 함수
    PPE 착용 여부에 따라 색상이 달라짐
    """
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)


# 메인 기능 함수

def detect_ppe(video_path):
    """
    비디오를 읽고, 사람과 PPE를 감지하고
    PPE를 제대로 착용했는지 판단하여 결과를 출력하는 함수
    """

    # 1. 모델 불러오기
    model = YOLO(Config.MODEL_PATH)
    names = model.names # 클래스 이름 캐싱

    # 2. 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("동영상 읽기 실패")
        return
    
    # 2-1. 누적 통계 초기화
    last_saved_time = datetime.now()
    total_count_acc = 0
    perfect_count_acc = 0
    frame_count_acc = 0
    
    # 3. 프레임 반복 처리
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 리사이즈 (성능 개선)
        frame = cv2.resize(frame, (640, 360))

        # 4. YOLO 모델로 객체 탐지 (사람, 안전모, 안전조끼)
        results = model(frame, verbose=False)
        result = results[0]

        # 결과 저장할 리스트
        person_boxes = []
        hardhat_boxes = []
        vest_boxes = []

        # 5. 결과에서 박스 정리
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])        # 클래스 ID
                conf = float(box.conf[0])       # 신뢰도
                label = model.names[cls_id]     # 클래스 이름

                if conf < Config.CONF_THRESHOLD:
                    continue    # 신뢰도 낮으면 무시함

                # 좌표 값 가져오기
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                bbox = (x1, y1, x2, y2)

                # 어떤 클래스인지에 따라 리스트에 저장
                if label == 'Person':
                    person_boxes.append(bbox)
                elif label == 'Hardhat':
                    hardhat_boxes.append(bbox)
                elif label == 'Safety Vest':
                    vest_boxes.append(bbox)

        # 6. 사람마다 PPE 착용 상태 확인하기
        perfect_count = 0   # 완벽 착용자 수

        for p_box in person_boxes:
            # 그 사람 박스 안에 안전모와 안전조끼가 있는지 확인
            has_hat = any(center_inside(h_box, p_box) for h_box in hardhat_boxes)
            has_vest = any(center_inside(v_box, p_box) for v_box in vest_boxes)

            color = Config.LABEL_COLORS['perfect'] if has_hat and has_vest else Config.LABEL_COLORS['imperfect']
            if has_hat and has_vest:
                perfect_count += 1
            draw_person_box(frame, p_box, color)
            
        # 7. 착용률 계산
        total = len(person_boxes)
        ratio = (perfect_count / total) * 100 if total > 0 else 0

        # 8. 화면에 통계 표시 (총 인원, 완벽 착용자 수, 퍼센트)
        draw_text(frame, f'Total: {total}', Config.TEXT_POS['total'], Config.TEXT_COLOR)
        draw_text(frame, f'Perfect: {perfect_count}', Config.TEXT_POS['perfect'], Config.LABEL_COLORS['perfect'])
        draw_text(frame, f'Ratio: {ratio:.1f}%', Config.TEXT_POS['ratio'], (0, 255, 255))

        # 경고 문구 출력 (2명 이상 미착용 시)
        if total - perfect_count >= 2:
            draw_text(frame, 'No Wearing', Config.TEXT_POS['alert'], Config.LABEL_COLORS['imperfect'], 0.9, 3)

        # 누적 통계 업데이트
        total_count_acc += total
        perfect_count_acc += perfect_count
        frame_count_acc += 1


        # 9. 결과 화면 출력
        cv2.imshow("PPE Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 10. 종료
    cap.release()
    cv2.destroyAllWindows()


# 실행 부분
if __name__ == "__main__":
    # 감지할 비디오 파일 경로 지정
    detect_ppe('../../img/hardhat1.mp4')