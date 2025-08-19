'''
yolo_test_img.py를 토대로 기능 추가
1. 총 인원 수, 완벽 착용 인원 수, 착용비율
'''

from ultralytics import YOLO
import time
import cv2

def detect_ppe(video_path):
    # YOLO 모델
    model = YOLO('best.pt')

    # 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("동영상 읽기 실패")
        return

    # 클래스 이름 정의
    ppe_classes = ['Hardhat', 'NO-Hardhat', 'Safety Vest', 'NO-Safety Vest']
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        # 객체 탐지
        results = model(frame)

        #img = cv2.imread(video_path)
        #detect_hardhat = False

        # 탐지 결과 반복
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]

                # 지정한 PPE 클래스에 속하는 경우만
                if label in ppe_classes and conf>0.5 :
                    #detect_hardhat = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                    # 클래스별 색상 구분
                    if label == 'Hardhat':
                        color = (0, 255, 0)
                    elif label == 'NO-Hardhat':
                        color = (0, 0, 255)
                    elif label == 'Safety Vest':
                        color = (0, 255, 255)
                    elif label == 'NO-Safety Vest':
                        color = (255, 0, 255)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{label} ({conf:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 결과 출력
        cv2.imshow("PPE Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_ppe('./img/hardhat1.mp4')