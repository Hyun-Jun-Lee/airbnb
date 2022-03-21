# Airbnb Clone Coding

<a href="https://www.airbnb-clone.site/">https://www.airbnb-clone.site/</a>

<a href="https://nomadcoders.co/airbnb-clone">노마드코더</a> 강의를 수강하며 Airbnb 홈페이지 Clone Coding

> Skils

- Django
- tawlind css
- AWS EC2

> 구현 기능

- Social Login(Github, KAKAO) 
- 조건에 맞는 Room 검색 
- Room 예약 및 예약 진행 상태 확인 (Confirm, Pending, Cancel) 

> Project Structure

- core : 자주 사용되는 기능들, Abstract Model로 각 모델이 생성 및 업데이트 시기 저장하는 기능, Custom Manager 명령어
- users : Social Login(Github, KAKAO) 기능, Profile 페이지 구현
- rooms :  Room 생성 및 검색, 사진 업로드 및 삭제 기능, 리뷰 평점, 캘린더 기능
- reservations : Room 예약 및 예약 진행 상태 확인(Confirm, Pending, Cancel)
- conversations : Direct Message 기능 구현 
