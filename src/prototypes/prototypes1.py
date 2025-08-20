# YOLO 모델을 불러오기 위한 라이브러리
from ultralytics import YOLO
# 비디오 처리와 화면 출력 등을 위한 OpenCV 라이브러리
import cv2

# 설정값
class Config:
    MODEL_PATH = 'best.pt'  # 사용할 YOLO 모델 파일 이름
    CONF_THRESHOLD = 0.3    # 정확도(신뢰도) 30% 이상만 인식에 사용
    TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX    # 텍스트 출력할 때 사용할 글씨체
    TEXT_COLOR = (255, 255, 255)            # 흰색 글씨
    FRAME_DELAY = 1                         # 프레임 간 간격

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

def is_inside(inner_box, outer_box):
    """
    작은 박스(inner)가 큰 박스(outer) 안에 완전히 들어가 있는지 확인하는 함수
    ex) 안전모 박스(inner)가 사람 박스(outer) 안에 들어가 있으면
    안전모를 착용했다고 판단
    """
    ix1, iy1, ix2, iy2 = inner_box  # 안쪽 박스 좌표
    ox1, oy1, ox2, oy2 = outer_box  # 바깥 박스 좌표
    return ix1 >= ox1 and iy1 >= oy1 and ix2 <= ox2 and iy2 <= oy2

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

    # 2. 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("동영상 읽기 실패")
        return
    
    # 3. 한 프레임씩 반복해서 읽기
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 4. YOLO 모델로 객체 탐지 (사람, 안전모, 안전조끼)
        results = model(frame)

        # 결과 저장할 리스트
        person_boxes = []
        hardhat_boxes = []
        vest_boxes = []

        