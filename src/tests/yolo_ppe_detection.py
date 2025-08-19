'''
yolo_test_img.py를 토대로 기능 추가
1. 총 인원 수, 완벽 착용 인원 수, 착용비율
'''

from ultralytics import YOLO
import cv2

'''
작은 박스(inner)가 큰 박스(outer)에 완전히 포함되는지 여부
예 : 안전모 박스가 사람 박스 안에 있는지 판단
'''
def is_inside(inner_box, outer_box):
    ix1, iy1, ix2, iy2 = inner_box
    ox1, oy1, ox2, oy2 = outer_box
    return ix1 >= ox1 and iy1 >= oy1 and ix2 >= ox2 and iy2 >= oy2

def detect_ppe(video_path):
    # YOLO 모델
    model = YOLO('best.pt')

    # 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("동영상 읽기 실패")
        return

    # 클래스 이름 정의
    #ppe_classes = ['Hardhat', 'NO-Hardhat', 'Safety Vest', 'NO-Safety Vest']
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        # 객체 탐지
        results = model(frame)

        # 탐지된 박스 저장용 리스트
        person_boxes = []
        hardhat_boxes = []
        vest_boxes = []

        # 탐지 결과 반복
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]

                if conf < 0.3:
                    continue    # 낮은 신뢰도 무시

                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 박스 좌표

                # 클래스에 따른 분류
                if label == 'Person':
                    person_boxes.append((x1, y1, x2, y2))
                elif label == 'Hardhat':
                    hardhat_boxes.append((x1, y1, x2, y2))
                elif label == 'Safety Vest':
                    vest_boxes.append((x1, y1, x2, y2))

        perfect_count = 0   # PPE 완벽 착용 인원 수

        # 각 사람에 대해 PPE 착용 여부 확인
        for p_box in person_boxes:
            has_hat = any(is_inside(h_box, p_box) for h_box in hardhat_boxes)
            has_vest = any(is_inside(v_box, p_box) for v_box in vest_boxes)

            if has_hat and has_vest:
                perfect_count += 1
                color = (0, 255, 0)

            else:
                color = (0, 0, 255)

            # 사람 박스 시각화
            x1, y1, x2, y2 = p_box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 통계 계산
        total = len(person_boxes)
        ratio = (perfect_count / total) * 100 if total > 0 else 0

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