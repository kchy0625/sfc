# SFC (School Face Check) - 학교 출석체크 얼굴인식 프로젝트

## 프로젝트 개요
- SFC(School Face Check)은 학교 출석체크를 얼굴인식 기술을 활용하여 자동화하고 관리하는 프로젝트입니다.
기존에는 교수님이 수업 시 출석부를 확인하기 위해 학생들의 이름을 일일이 호명해야 했으며,
- 출석 데이터를 관리하는 것도 번거로웠습니다.
- 이를 해결하기 위해 얼굴인식 기술을 도입하여 학생의 얼굴을 인식하고 출석체크 및 관리를 자동화하고자 합니다.

## 주요 기능
- 학생이 회원 가입 시 얼굴 이미지를 등록하고, 이를 통해 얼굴 데이터를 추출하여 저장합니다.
- 교수님이 강의 시 수업 참여 여부를 얼굴인식을 통해 확인할 수 있습니다.
- 학생은 자신의 출석 결과를 확인할 수 있고, 교수님은 엑셀 파일로 출결 데이터를 다운로드할 수 있습니다.
- 출결에 문제가 있을 경우 교수님에게 메시지를 보낼 수 있는 기능을 제공합니다.

## 아키텍처
![image](https://github.com/kchy0625/sfc/assets/56716209/ad319aa4-1e72-4582-b0e1-afc3ca0334b0)

## 프로젝트 개발 환경
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 

<img src="https://img.shields.io/badge/anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> <img src="https://img.shields.io/badge/dlib-00b450?style=for-the-badge&logo=dlib&logoColor=white">  <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"> <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white">

- Python과 Django 웹 프레임워크를 사용하여 개발되었습니다.
- 얼굴 인식에는 Dlib과 Face recognition 라이브러리를 사용하였습니다.
- 데이터베이스는 MySQL을 사용하여 구축되었습니다.
## 프로젝트 구성
- 웹 페이지를 통해 얼굴 인식 및 출석체크를 진행합니다.
- MySQL Workbench를 사용하여 데이터베이스의 EER 다이어그램을 설계하였습니다.
- 프로젝트의 전체 구성도 및 Usecase Diagram을 작성하여 개발 과정을 시각화하였습니다.


![image](https://github.com/kchy0625/sfc/assets/56716209/aa6ff2f8-7eed-4bd0-b71a-30c0cd413602) ![image](https://github.com/kchy0625/sfc/assets/56716209/b37bb19f-467f-45b0-b2a8-d25c2712bf1b)

## 구현 화면
![image](https://github.com/kchy0625/sfc/assets/56716209/c2b504f9-b37d-474f-a426-c2c0ca5a4075)![image](https://github.com/kchy0625/sfc/assets/56716209/905e3380-d68b-44ad-8967-4dbe91341f66)![image](https://github.com/kchy0625/sfc/assets/56716209/ba290990-8845-4be8-bc87-8985abd6c8af)
 - 로그인화면, 출석여부, csv파일 




## 실험 및 고찰
- 얼굴 인식 및 출석체크 기능을 구현하고 실험을 통해 학번 및 인식률을 확인하였습니다.
- 출석 확인 시 날짜와 학생의 출결 상태를 확인할 수 있으며, 엑셀로 데이터를 저장할 수 있도록 구현하였습니다.
## 결론 및 향후 과제
- 현재 개발 환경의 한계로 인해 GPU를 활용한 얼굴 학습이 제한되어 있습니다. 향후 성능이 우수한 서버 및 카메라를 활용하여 얼굴 인식 기능을 개선할 예정입니다.
- 서버를 구축하여 다양한 기기에서 얼굴 인식 기능을 활용할 수 있도록 할 계획입니다. 또한 3D 얼굴 인식 기술을 적용하여 인식률을 높일 것입니다.
## 참고 자료
- FaceNet을 이용한 얼굴 인식 시스템 개발
- Django 웹 프레임워크 공식 문서
- Face recognition 라이브러리 공식 GitHub 페이지
