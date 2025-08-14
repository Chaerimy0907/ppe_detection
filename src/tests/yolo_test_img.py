'''
opencv로 테스트했을 때 안전모가 아닌 부분까지 감지되어
yolo를 사용해 조금 더 정밀한 감지 테스트
'''
from ultralytics import YOLO
import cv2

def detect_yellow_hardhat(img_path):

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_yellow_hardhat('./img/1.jpg')