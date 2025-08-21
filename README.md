# PPE DETECTION CCTV

PPE(Personal Protective Equipment, 개인 보호 장비) 착용 여부를 YOLOv8 기반으로 감지하는 실시간 CCTV 모니터링 시스템   
작업자의 안전모 및 안전조끼 착용을 자동 감지하고, 실시간 통계 출력 및 착용 비율을 CSV 파일로 기록하여 산업 현장의 안전사고 예방에 기여

---

## 프로젝트 목표

- **YOLOv8 기반 객체 감지 모델을 이용한 PPE 착용 여부 실시간 감지**
- 감지된 인원 중 **PPE를 완벽히 착용한 인원 수 및 착용 비율 출력**
- 미착용 인원이 일정 수 이상일 경우 **경고 메시지 출력**
- 일정 주기마다 **착용률 통계 및 평균 인원 수를 CSV로 저장**

---

## 주요 기능

- 객체 감지 클래스 : `Person`, `Hardhat`, `Safety Vest`
- 각 사람 박스 내부에 안전모와 안전 조끼가 있는지 확인하여 **PPE 완전 착용 여부 판단**
- 실시간 영상에 통계 수치와 색상 시각화 출력:
  - **초록 박스** : 안전모 + 안전조끼 착용 (완전 착용자)
  - **빨간 박스** : 미착용 또는 일부 미착용
- **경고 기능** : 미착용자 2명 이상일 경우 경고 문구 출력
- **10초마다 CSV 저장** (실제 사용 시 1시간 단위로 조정 가능) :
  - 평균 인원 수
  - 평균 착용률(%)
  > 예시 : `ppe_log.csv` → `2025-08-21 14:00:00, 9, 87.5`

---

## 설정값 (`Config` 클래스)

| 항목 | 설명 | 기본값 |
|------|----------|-------|
| `MODEL_PATH` | 학습된 YOLOv8 모델 경로 | `'../../models/best.pt'` |
| `CSV_PATH` | 착용률 저장용 CSV 경로 | `'./ppe_log.csv'` |
| `CONF_THRESHOLD` | 감지 신뢰도 임계값 | `0.4` |
| `FRAME_DELAY` | 프레임 간 대기 시간 (ms) | `5` |
| `LABEL_COLOR` | 착용/미착용 색상 설정 | 초록 / 빨강 |

---

## 하드웨어 / 설치 및 실행 방법

### 1. 하드웨어
- 웹캠 (웹캠으로 테스트를 진행할 수 없는 환경이라 mp4 파일로 테스트 진행)
- 데스크탑

### 2. 설치

```bash
pip install ultralytics opencv-python
```

### 3. 파일 구성

```
ppe_detection/
├── assets
├── docs
├── feedback
├── img
│   └── hardhat1.mp4         # 테스트 영상
├── models
│   └── best.pt              # 학습된 YOLOv8 모델
├── src
│   └── final
│       └── main.py          # 실행 파일
│       └── ppe_log.csv      # 착용률 기록 파일 (자동 생성)
│   └── prototypes
│   └── tests 
```

### 4. 실행

```bash
python scr/final/main.py
```

> `prototypes1.py` 내부에 `VIDEO_PATH`, `MODEL_PATH`가 하드코딩 되어 있으므로 필요시 수정

---

## 저장되는 CSV 형식

| Timestamp           | Average Total People | Average Perfect Ratio (%) |
| ------------------- | -------------------- | ------------------------- |
| 2025-08-21 14:00:00 | 8                    | 87.5                      |

- **주기** : 기본 10초 (테스트 용도) 실사용 시 1시간으로 조정 가능
- **비율 기준** : 완전 착용자 수 / 전체 인원 x 100
- **판단 기준** : PPE 두 가지(Hardhat + Safety Vest)가 모두 있어야 착용으로 인정됨

---

## 테스트 방법

1. `models/best.pt` → [사전 학습된 모델](https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection/tree/main/models) 다운로드
2. `img/hardhat1.mp4` → 테스트용 영상 준비
3. `python src/fianl/main.py` 실행
4. 영상 재생 화면에서 사람마다 색상 박스와 통계 수치 확인
5. 'q' 키를 누르면 종료되며, 통계는 자동 저장됨

---

## 진행상황
<details>
<summary>피드백 로그</summary>

- [0814 - 피드백 진행](/feedback/0814.md)
- [0818 - 피드백 진행](/feedback/0818.md)
- [0819 - 피드백 진행](/feedback/0819.md)
- [0820 - 피드백 진행](/feedback.0820.md)

</details>

<details>
<summary>코드 진행 상황</summary>

- [0820 - Prototype 코드 작성](src/prototypes/prototypes1.py)
- [0820 - 성능 최적화 코드 작성](src/prototypes/prototypes2.py)
- [0821 - CSV 통계 저장 기능 추가 및 코드 정리](src/prototypes/prototypes3.py)
- [0821 - 코드 최적화 후 main.py 작성](src/final/main.py)

</details>

---

## 향후 개선 아이디어

- 미착용자에 대한 **지속 시간 추적 및 기록**
- 미착용 상태가 일정 시간 이상 지속될 경우 **알람 또는 자동 저장**
- **야간 또는 어두운 환경**에서도 잘 작동하도록 모델 재학습
- **모듈화 및 웹 대시보드 연동** (Flask, Streamlit 등)

---

## 참고 사항

- YOLO의 감지 신뢰도(confidence) 임계값은 낮추면 더 많이 감지되지만 오류도 증가함
- 단순 중심점 기준 착용 여부 판단이기 때문에 **겹쳐 보이는 객체는 오탐지 발생 가능**
- 감지된 총 인원은 고유 추적이 아닌 "프레임 내 감지 기준"임