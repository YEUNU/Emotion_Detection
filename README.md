# Emotion_Detection

## 기술스택

<div align=left> 
  <img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visual studio code&logoColor=white"> 
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
  <img src="https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white"> 
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> 
</div>

## 프로젝트 개요

### 프로젝트 설명

K-digital Training 교육생 "VALUE UP" 공모전용 프로젝트

### 프로젝트 기간

2023.04.13 ~ 2023.05.14

### 프로젝트 목표

사용자의 감정분석 + GPT를 활용한 개인 맞춤형 감정적 대화 챗봇서비스 구현

## 프로젝트 결과

| 메인 화면 | 회원가입 | 채팅창 | STT | 사용자 입력 | GPT 결과 |
| --- | --- | --- | --- | --- | --- |
| <img src="https://user-images.githubusercontent.com/61678329/251390764-acd21dab-8451-43a7-8ef3-e3ac0c63a8dc.png" width="300px"> | <img src="https://user-images.githubusercontent.com/61678329/251390771-f552e40f-2027-42d4-9b13-5078a3c37261.png" width="300px"> | <img src="https://user-images.githubusercontent.com/61678329/251390773-4b3779c1-e2dd-4a8f-bbb3-f11be2a64d4c.png" width="300px"> | <img src="https://user-images.githubusercontent.com/61678329/251390781-f2cd9bac-a019-4f61-94d9-d72f483b3835.png" width="300px"> | <img src="https://user-images.githubusercontent.com/61678329/251390782-c1aa4c8c-92ac-448f-a44d-236bbeea335e.png" width="300px"> | <img src="https://user-images.githubusercontent.com/61678329/251390784-faf8aae7-0224-4039-8e21-1cb47aa542f0.png" width="300px">|  

| 결과 영상 |
|:-:|
| <a href="https://user-images.githubusercontent.com/61678329/252132385-856edf36-12fc-4861-8f3a-41ea72cebbfe.mp4" target="_blank" rel="noopener noreferrer"><img src="https://user-images.githubusercontent.com/61678329/251390764-acd21dab-8451-43a7-8ef3-e3ac0c63a8dc.png" width="320" alt="결과 영상"></a> |
## AI
### STT
Whisper Model 사용
| Whisper Reference |
|:-:|
|https://github.com/openai/whisper|
### GPT Prompt Engineering
GPT 3.5 Turbo Model 사용
| GPT Reference |
|:-:|
|[https://github.com/openai/whisper](https://platform.openai.com/docs/guides/gpt)|
### 감정분석
#### 데이터셋
| 감성 대화 말뭉치| 감정 분류를 위한 대화 음성 데이터셋 |
|---| --- |
|https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=86|https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=263|
#### 학습 방법
KoBert Fine Tuning  
    Dropout : 0.5  
    Learning Rate : 2e-5,  
    Weight Decay : 1e-2,  
#### 학습 결과

| Confusion Matrix | Bar Graph |
| --- | --- |
| ![Confusion Matrix](https://user-images.githubusercontent.com/61678329/252130299-e329ce4a-aa2e-4908-a2cd-4345f2dd2423.png) | ![Bar Graph](https://user-images.githubusercontent.com/61678329/252132321-cc2699af-ad9f-41b4-9075-30472ca78383.png) |




