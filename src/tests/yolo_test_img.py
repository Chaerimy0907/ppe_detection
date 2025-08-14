'''
opencv로 테스트했을 때 안전모가 아닌 부분까지 감지되어
yolo를 사용해 조금 더 정밀한 감지 테스트
'''
from ultralytics import YOLO
import cv2

def detect_yellow_hardhat(img_path):
    # YOLO 모델
    model = YOLO('best.pt')

    # 클래스 이름 정의
    hardhat_classes = ['Hardhat', 'NO-Hardhat']
    results = model(img_path)

    img = cv2.imread(img_path)
    detect_hardhat = False

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]

            if label in ['Hardhat', 'NO-Hardhat'] and conf>0.5 :
                detect_hardhat = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                color = (0, 255, 0) if label == 'Hardhat' else (0, 0, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{label} ({conf:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # if detect_hardhat:
    #     cv2.putText(img, "Hardhat O", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    # else:
    #     cv2.putText(img, "Hardhat X", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Detection Hardhat", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_yellow_hardhat('./img/1.jpg')