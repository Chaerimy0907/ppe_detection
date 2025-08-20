# PPE DETECTION CCTV

PPE(Personal Protective Equipment, 개인 보호 장비) 착용 여부를 YOLOv8 기반으로 감지하고, 실시간 모니터링 및 착용 통계를 시각화하는 시스템   
현장에서의 안전사고 예방을 목적으로 함

---

## 프로젝트 목표

- 작업자의 **안전모(Hardhat)**, **안전조끼(Safety Vest)** 착용 여부 감지
- 전체 인원 대비 PPE 완벽 착용자 수와 비율을 실시간 출력
- 미착용 인원이 일정 수 이상일 경우 경고 문구 출력

---

## 진행사항
<details>
<summary>피드백</summary>

- [0814 - 피드백 진행](/feedback/0814.md)
- [0818 - 피드백 진행](/feedback/0818.md)
- [0819 - 피드백 진행](/feedback/0819.md)
- [0820 - 피드백 진행](/feedback.0820.md)

</details>

<details>
<summary>코드 진행 사항</summary>

- [0820 - Prototype 코드 작성](src/prototypes/prototypes1.py)

</details>

---

## 하드웨어 / 설치 및 실행

### 1. 하드웨어
- 웹캠 (웹캠으로 테스트를 진행할 수 없는 환경이라 mp4 파일로 테스트 진행)
- 데스크탑

### 2. 설치

```bash
pip install ultralytics opencv-python
```

### 3. 실행 (prototype)
```bash
python prototypes1.py
```

> `prototypes1.py`에서 사용할 비디오 경로와 모델 경로를 `../../models/best.pt`, `../../img/hardhat1.mp4`

---

## 주요 기능 설명

- YOLO 모델을 통한 객체 탐지
- 객체 클래스 : `Person`, `Hardhat`, `Safety Vest`
- 각 사람 박스 내부에 안전모와 안전조끼가 있는지 확인하여 PPE 착용 여부 판단
- 실시간 영상에 통계 수치와 색상 시각화 표시
  - 초록 박스 : 안전모 + 안전조끼 착용자
  - 빨간 박스 : 미착용자
- 미착용자가 2명 이상일 경우 화면 하단에 경고 출력

---

## 설정값 (`Config` 클래스)

| 항목 | 설명 | 기본값 |
|------|----------|-------|
| `MODEL_PATH` | 학습된 YOLOv8 모델 경로 | `best.pt` |
| `CONF_THRESHOLD` | 신뢰도 임계값 | 0.3 |
| `FRAME_DELAY` | 프레임 간 대기 시간 (ms) | 1 |
| `TEXT_FONT` | 텍스트 폰트 | `cv2.FONT_HERSHEY_SIMPLEX` |
| `TEXT_COLOR` | 기본 텍스트 색 | 흰색 |
| `LABEL_COLOR` | 착용/미착용 색상 설정 | 초록/빨강 |

---

## 폴더 구조

```
ppe_detection/
├── assets
├── docs
├── feedback
├── img
│   └── hardhat1.mp4     # 테스트 영상
├── models
│   └── best.pt              # 학습된 YOLOv8 모델
├── src
│   └── final
│   └── prototypes
│       └── prototypes1.py 
│   └── tests 
```

---

## 사용법 가이드

1. `best.pt`라는 이름의 YOLOv8 모델이 필요함. [github에 공개된 모델](https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection/tree/main/models)
2. `img/` 폴더에 테스트용 영상 저장
3. `prototypes1.py`를 실행하면 영상이 열리고 감지된 인원이 화면에 박스로 표시됨
4. 사람마다 초록/빨간 박스로 표시되며, 상단에는 총 인원, 착용 인원, 착용 비율이 출력됨
5. 'q' 키를 누르면 프로그램이 종료됨

---

## 참고사항

- `is_inside()` 함수는 객체 박스가 사람 박스 내부에 **완전히** 포함되는지 판단함
- `Config` 클래스를 통해 모든 하드코딩값을 한 곳에서 조정 가능하게 작성함
- 전처리나 후처리 단계 추가, 저장 기능 확장도 쉽게 구현 가능함

---

## 향후 개선 아이디어

- 미착용자 별 **미착용 지속 시간 기록**
- 일정 시간 이상 미착용 시 **csv에 자동 저장**
    > 인식 오류 이슈로 착용했음에도 감지가 안 되는 시간까지 카운트되어 정확하지 않음.
- 야간 및 악천후 대응을 위한 모델 재학습