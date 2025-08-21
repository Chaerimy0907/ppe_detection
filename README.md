# PPE DETECTION CCTV

PPE(Personal Protective Equipment, 개인 보호 장비) 착용 여부를 YOLOv8 기반으로 감지하고, 실시간 모니터링 및 착용 통계를 시각화하는 시스템
건설현장, 공장 등에서 **작업자의 안전사고 예방**을 주요 목적으로 설계

---

## 프로젝트 목표

- 작업자의 **안전모(Hardhat)**, **안전조끼(Safety Vest)** 착용 여부 감지
- 전체 인원 대비 PPE **완벽 착용자 수** 및 **착용 비율** 실시간 출력
- **미착용 인원 2명 이상일 경우 경고 문구** 출력
- **10초마다 평균 인원/착용률 통계 CSV 저장**

---

## 참고 모델

- 사용된 YOLOv8 모델은 다음 GitHub에서 확인 및 다운로드 가능 :
  [github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection](https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection/tree/main/models)

---

## 하드웨어 및 설치

### 1. 하드웨어 요구 사항
- 웹캠 (또는 사전 녹화된 mp4 영상)
- 데스크탑 또는 노트북

### 2. 패키지 설치

```bash
pip install ultralytics opencv-python
```

---

## 실행 방법

```bash
python scr/final/main.py
```

> `prototypes1.py` 파일 내의 비디오 경로 및 모델 경로
> - 모델 경로 : `../../models/best.pt`
> - 비디오 경로 : `../../img/hardhat1.mp4`

---

## 폴더 구조

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

---

## 테스트 및 결과 확인

- 결과 화면에서는 실시간 감지된 사람 수 및 PPE 착용 여부가 시각적으로 표현됨
- `ppe_log.csv` 파일에는 10초 단위로 아래와 같은 통계가 저장됨 :

```csv
Timestamp,Average Total People,Average Perfect Ratio (%)
2025-08-21 15:48:20,2,50.0
2025-08-21 15:38:30,2,100.0
...
```

- **주기** : 기본 10초 (테스트 용도) 실사용 시 1시간으로 조정 가능
- **비율 기준** : 완전 착용자 수 / 전체 인원 x 100
- **판단 기준** : PPE 두 가지(Hardhat + Safety Vest)가 모두 있어야 착용으로 인정됨

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| **YOLOv8 기반 객체 감지** | `Person`, `Hardhat`, `Safety Vest` 세 가지 클래스를 실시간 감지 |
| **착용 여부 판단 방식** | 감지된 PPE 객체의 중심 좌표가 사람 박스 안에 있는지 여부로 착용 판단 |
| **실시간 시각화** | 초록색 박스 : PPE 완벽 착용 / 빨간색 박스 : 미착용 또는 일부 미착용 |
| **통계 시각화** | 총 인원 수, PPE 착용자 수, 착용률(%)을 화면에 표시 |
| **경고 기능** | 미착용자가 2명 이상일 경우 경고 문구 출력 |
| **CSV 저장** | 10초 단위로 평균 인원 수와 PPE 착용률을 CSV에 저장 (`./ppe_log.csv`) |

---

## 설정값 (`Config` 클래스)

| 항목 | 설명 | 기본값 |
|------|----------|-------|
| `MODEL_PATH` | 학습된 YOLOv8 모델 경로 | `'../../models/best.pt'` |
| `CSV_PATH` | CSV 저장 경로 | `'./ppe_log.csv'` |
| `CONF_THRESHOLD` | 감지 신뢰도 임계값 | `0.4` |
| `FRAME_DELAY` | 프레임 간 대기 시간 (ms) | `5` |
| `TEXT_FONT` | 텍스트 폰트 설정 | `cv2.FONT_HERSHEY_SIMPLEX` |
| `TEXT_COLOR` | 텍스트 기본 색상 | 흰색 |
| `LABEL_COLOR` | 박스 색상 설정 | 초록(완벽 착용) / 빨강(미착용 또는 일부 착용) |
| `TEXT_POS` | 영상 내 텍스트 출력 위치 | 좌상단 기준 고정 좌표들 |

---

## 성능 최적화 전후 비교

| 항목 | 최적화 전 | 최적화 후 |
|------|------------|-----------|
| **PPE 감지 정확도** | 동일 인물 중복 카운트 문제 | 평균값 기반으로 실제 인원과 유사 |
| **프레임 리사이즈** | 비디오의 원본을 사용 | 640x360으로 리사이즈 |
| **프레임 간 대기 시간** | 1 ms | 5 ms |
| **저장 항목** | 없음 | 평균 총 인원 수, 평균 착용률(%) |

> 프레임 기반 통계에서 **평균값 기반 시간 통계**로 변경하여 현실성 있는 결과 도출

---

## PPE 착용률

### 현실적인 감지 한계
- 빠르게 움직이는 사람, 가려진 시야, 조명 조건 등으로 감지 누락 발생
- YOLO 기반 실시간 감지는 **100% 감지 성공이 사실상 불가능**
- 완벽 감지율을 기준으로 하면 오탐/누락으로 인해 **과잉 경고** 발생

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

## 참고 사항

- YOLO의 감지 신뢰도(confidence) 임계값은 낮추면 더 많이 감지되지만 오류도 증가함
- 단순 중심점 기준 착용 여부 판단이기 때문에 **겹쳐 보이는 객체는 오탐지 발생 가능**
- 감지된 총 인원은 고유 추적이 아닌 "프레임 내 감지 기준"임

---

## 향후 개선 아이디어

- 미착용자에 대한 **지속 시간 추적 및 기록**
- 미착용 상태가 일정 시간 이상 지속될 경우 **알람 또는 자동 저장**
- **야간 또는 어두운 환경**에서도 잘 작동하도록 모델 재학습
- **모듈화 및 웹 대시보드 연동** (Flask, Streamlit 등)