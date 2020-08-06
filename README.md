# Introduction
* 대한민국 대표 주거정보 플랫폼 [직방](https://www.zigbang.com/) 클론 프로젝트
* 개발기간 : 2020.07.06 ~ 2020.07.17(12일)
* 개발인원 : Front-end 3명(송민규, 최지원, 현정호), Back-end 3명(김환일, 노광오, 정나온)
* [Front-end Github](https://github.com/wecode-bootcamp-korea/9-zookbang-frontend)
* [Back-end Github](https://github.com/wecode-bootcamp-korea/9-zookbang-backend)

# Purpose
- 스크럼 등 실무에서 사용하는 개발 방법론을 통해 협업 방식을 익힌다.
- 데이터 양이 많은 서비스를 클론하면서 데이터를 다루는 방식을 익힌다.
- 위치 정보(좌표) 기반 기능, 필터링, 검색 등 타겟 사이트 핵심 기능을 구현하며 백엔드 개발자로서 역량을 키운다.

# Demo Video
[![Demo](https://cdn.glitch.com/b267435c-fe08-4f53-8ded-95a7233fa13f%2Fzigbang-demo.png?v=1595485209854)](https://www.youtube.com/watch?v=kQA25QKZKUQ)

# Modeling
![Modeling](https://cdn.glitch.com/b267435c-fe08-4f53-8ded-95a7233fa13f%2Fzookbang_20200718_38_32.png?v=1595065302156)

# Technologies
* Python
* Django
* Bcrypt
* JWT
* KAKAO social login
* MySQL
* CORS headers
* Git, Github
* AWS EC2, RDS
* Docker

# Features
* account
	- 유저정보 저장
  - 회원가입 / 로그인
  	- 유효성 검사
    - 패스워드 암호화
    - 로그인 시 JWT Access 토큰 발행
		- 카카오 소셜 로그인
		- 문자 인증
  - 로그인 상태인지 확인하는 데코레이터 함수
 
* map
  - 중심 좌표 주변 2km 내 매물 표시 및 매물 목록 구현
	- 매물 상세정보 구현
   
* search
	- 검색 기능 구현
		- 건물, 지역, 학교, 지하철역 검색

* Docker에 프로젝트 빌드하여 배포
* AWS RDS DB 세팅
* unit test 진행
* git rebase로 프로젝트 관리

# API Documentation
https://documenter.getpostman.com/view/11638473/T1Djjei7
