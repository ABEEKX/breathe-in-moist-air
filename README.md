

## 0. 명칭 (제목, 이름)
#### Title: breathe-in-moist-air

## 1. 배경(문제)

1. 기존 중앙 난방의 문제점
- 교실의 온, 습도의 변화에 유연하게 대처하지 못한다.
- 교실의 학생이 건조하다/ 공기가 탁하다고 느끼는 시점은 이미 습도나 이산화탄소 농도가 이상 상태이다.
--> 따라서 온습도 및 이산화탄소 농도에 대한 적절한 예측과 조치가 필요하다.

2. 금전적 비효율
- 단위 시간 당 같은 난방 비용이라 할 때 각 교실마다 난방 수요가 필요할 때 집중적으로 난방을 하는것보다 모든 교실이 동일한 난방 스케줄을 가진 중앙 난방 시스템이 더 많은 비용이 들 것이다.
- 동일 난방비용일 때 중앙 난방시스템은 개별 난방시스템보다 사용자의 만족도가 낮다.

3. 쾌적한 공기가 학습에 미치는 영향
- 
- 


## 2. 주요 내용
- 온습도, CO2, 미세먼지 데이터를 수집한다.
- <5분 뒤> 상태를 <예측>한다.
- 온습도 예측 데이터를 바탕으로 가습기를 작동시킨다.
- CO2, 미세먼지 예측 데이터를 바탕으로 환기 알림을 준다.


## 3. 가치
- 쾌적한 공기 환경을 제공하는데 중앙난방의 문제점을 보완할 수 있다.
- 예측값을 활용해 문제가 되는 실내 공기 상태를 미연에 방지할 수 있다. 


## 4. 기술구조
- 온습도 센서 데이터의 축적 --> AWS 서버로
- 모인 데이터의 활용 : 예측

### 필요한 센서
- 온습도 센서: DHT22
- CO2센서: MH-Z14

### 필요한 액튜에이터
- 칼라 LED
- 피에조 부저
- 릴레이

## 5. 일정
- 18/01/02 ~ 18/01/05 제안서 ver1.0, 센서 및 액튜에이터 가동 실험
- 18/01/06 ~          데이터 수집
- 18/01/08 ~ 18/01/12 데이터 추이 파악 및 학습, 알림창 제작
- 18/01/15 ~ 18/01/16 포스터 정리 및 발표       

## 6. 역할분담
- 김민섭 : 팀장, CO2센서 작동 관리
- 박형준 : 액츄에이터 관리, 머신러닝 리더
- 장보우 : 온습도센서 작동 관리, 개발문서 관리


### 참고자료
* https://www.healthline.com/health/stuffy-nose-relief#humidifier
* search google for "MD format" or "Edit MD" etc...
https://pandao.github.io/editor.md/en.html would help.
