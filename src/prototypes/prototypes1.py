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