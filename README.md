

## 0. 명칭

### AIR MAN(Air Managing and Advisory ageNt)

- 학습 능률에 영향을 주는 온도와 CO2의 5분뒤 값을 예측하여, 온도를 미리 조절하고, CO2수치가 올라가기 전에 환기 알림을 준다. 이를 통해 독서실을 사용하는 학생의 학습 효과를 상승시키고, co2라는 변수를 고려하지 않는 기존 독서실과 차별을 두어 홍보에 도움을 줄수있다.

<br/>



## 1. 배경


#### 독서실 온도는 학생의 학습 효과에 영향을 끼친다.

- 뇌활성도는 덥거나 춥지 않은 적정온도(26도)일때 높아지며, 이 때 학습과 집중력에 관련된 베타파가 나와 효율적인 공부를 돕는다.([KBS1 과학카페 뇌파실험](http://www.laxtha.com/SiteInfoListOneView.asp?infid=620))

#### CO2의 수치 또한 학생의 학습 효과에 영향을 끼친다.

- 환기를 하지 않는 교실은 이산화탄소 농도가 4,000 ppm 이상 도달하며, 이는 [학교 보건법 시행규칙](http://www.law.go.kr/%EB%B2%95%EB%A0%B9/%ED%95%99%EA%B5%90%EB%B3%B4%EA%B1%B4%EB%B2%95%20%EC%8B%9C%ED%96%89%EA%B7%9C%EC%B9%99) 에서 규정하고 있는 1,000ppm의 4배 정도의 수치이다. 이산화탄소 농도가 높은 환경에 짧은 시간 노출되더라도 학업수행능력에 영향을 받을 수 있다.([교실 내 공기 중 이산화탄소 농도가 학습에 미치는 효과에 대한 문헌 연구. 임완철. 2015](https://goo.gl/8ogCHN))

#### 예측 시스템의 필요성

- 학생이 춥거나 덥다고 생각하거나, 공기가 답답하다고 느끼면, 이미 그로인해 집중력이 흐트러지게된다.

- 적정 온도를 유지하기 위해서, 온도 변화를 예측하여 미리 온도를 조절할 수 있는 시스템이 필요하다.

- 짧은 시간 노출되어도 학습효과에 좋지않은 영향을 줄 수 있는 높은 CO2농도에 대비하기 위해, 해당 수치가 올라가기 전에 미리 환기를 할 수 있어야한다.

<br/>

## 2. 주요 내용
- 독서실의 온도, CO2, 미세먼지 데이터를 수집한다.
- 독서실의 5분 뒤 온도와 CO2 상태를 예측한다.
- 만약 5분뒤 예측온도가 적정온도(26도)를 벗어날 경우, 관리자에게 팝업창을 통해 온도를 조절하라는 알림을 준다.
- 만약 5분뒤 예측CO2 농도가 적정농도(1000ppm)보다 높아질 경우, 관리자에게 팝업창을 통해 환기를 시키라는 알림을 준다.
- 단, 독서실 내부의 미세먼지수치보다 [에어코리아](http://www.airkorea.or.kr/index)에서 제공한 해당지역의 미세먼지 수치가 더 높을 경우, 환기를
 시키라는 알림을 주지 않는다.
 
<br/>

## 3. 가치

- 온도변화에 미리 대응하지 못해 일정한 적정온도를 유지하지 못하고, CO2 수치를 고려하지 못하는 기존 독서실 시스템과 차별화를 두어, 독서실 홍보에 도움이 될 수 있다.

<br/>

## 4. 기술구조

- 독서실의 온도,CO2,미세먼지 센서 데이터를 AWS Ubuntu 서버의 mySQL 데이터베이스에 축적한다.
- 크롤링을 이용해 http://www.airkorea.or.kr/index 에서, 강의실 바깥의 미세먼지 데이터를 제공받는다.
- LSTM(Long Short Term Memory)을 이용하여 5분뒤 온도와 CO2농도를 예측한다.

#### 필요한 센서
- 온습도 센서: DHT22
- CO2센서: MH-Z14

<br/>

## 5. 일정
- 18/01/02 ~ 18/01/06 제안서 ver1.0, 센서 및 액튜에이터 가동 실험
- 18/01/06 ~ 18/01/12 데이터 수집
- 18/01/08 ~ 18/01/12 데이터 추이 파악 및 학습, 알림창 제작
- 18/01/15 ~ 18/01/16 포스터 정리 및 발표       


<br/>

## 6. 역할분담
- 김민섭 : 팀장, 문서관리, 크롤링개발
- 박형준 : 액츄에이터 관리, 머신러닝 리더
- 장보우 : 온도, 미세먼지,CO2 센서 작동 관리, 알림시스템 개발

<br/>


