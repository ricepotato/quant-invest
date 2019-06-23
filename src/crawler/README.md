# crawler
crawler

한달에 한번씩 실행후 DB 에 저장

http://comp.fnguide.com/SVO2/asp/SVD_Main.asp

위 사이트에서 crawling

필요한 데이터

코스닥/코스피 전체 기업 목록 필요

전체기업의 

ROA, ROE, 시가총액, PER, PBR, EV/EVITA, 


 
 ## 전체 종목 가져오는 방법
 '한국거래소' 사이트 이용 

 http://marketdata.krx.co.kr

 시장정보 -> 상장현황 -> 상장회사 검색 으로 들어가서 '시장구분' 에서 '전체' 클릭 후 '조회' 버튼 클릭 한 다음 Excel 또는 csv 로 다운로드

## 코스닥/코스피 구분 어케하는지?
코스피 코스닥 따로 다운로드 받아 종목 databse 에 저장

## 공익기업주/금융기업 구분 가능한지?
금융기업은 업종코드를 보고 구분할 수 있음, 공익기업은 확인 필요
