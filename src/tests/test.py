'''
1일차 목표 : 웹캠으로 노란색 안전모 감지하여 착용여부 표시
색상 범위 HSV 기준
면적 필터링 : 노이즈 제거

# 1단계 : 노란색 안전모 검출
- 테스트를 위해 사진으로 감지 실행
'''
import cv2
import numpy as np

# 노란색 안전모 감지 함수
def detect_yellow_hardhat(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_lower = (20, 100, 100)
    yellow_upper = (30, 255 ,255)

    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = False
    for cnt in contours:
        if cv2.contourArea(cnt) > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            detected = True
    return frame, detected

# 감지 실행 함수
def detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result_frame, is_detected = detect_yellow_hardhat(frame)

        if is_detected:
            msg = "Hardhat O"
            color = (0, 255, 0)

        else:
            msg = "Hardhat X"
            color = (0, 0, 255)

        cv2.putText(result_frame, msg, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.imshow("Yellow Hardhat Detection", result_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":