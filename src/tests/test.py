'''
1일차 목표 : 웹캠으로 노란색 안전모 감지하여 착용여부 표시
색상 범위 HSV 기준
면적 필터링 : 노이즈 제거

# 1단계 : 노란색 안전모 검출
'''
import cv2
import numpy as np

# 노란색 안전모 감지 함수
def detect_yellow_hardhat(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_lower = (20, 100, 100)
    yellow_upper = (30, 255 ,255)

# 감지 실행 함수
def detection():

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=="__main__":