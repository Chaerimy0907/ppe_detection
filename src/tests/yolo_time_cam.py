from ultralytics import YOLO
import time
import cv2

def detect_hardhat(video_path):
    # YOLO 모델
    model = YOLO('best.pt')

    # 클래스 이름 정의
    #class_names = model.names
    
    # 객체 탐지
    #results = model(img_path)

    #img = cv2.imread(img_path)
    #detect_hardhat = False

    # 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("동영상 읽기 실패")
        return
    
    # FPS 값 추출 (프레임 간 시간 계산용)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 / fps    # 한 프레임당 걸리는 시간

    # 착용 시간 누적 변수
    wear_time = 0

    # 연속 미착용 프레임 수를 카운트하기 위한 변수
    no_wear_count = 0

    # 경고 기준 : 5초 동안 미착용
    no_wear_threshold = int(fps * 3)

    # 탐지 결과 반복
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]

            # 안전모만 필터링
            if label in ['Hardhat', 'NO-Hardhat'] and conf>0.5 :
                detect_hardhat = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 색상 구분
                color = (0, 255, 0) if label == 'Hardhat' else (0, 0, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{label} ({conf:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # if detect_hardhat:
    #     cv2.putText(img, "Hardhat O", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    # else:
    #     cv2.putText(img, "Hardhat X", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # 결과 출력
    cv2.imshow("Detection Hardhat", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_yellow_hardhat('./img/1.jpg')