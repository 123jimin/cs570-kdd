# KDD
## 패키지
`pip`로 `numpy`, `scipy`, `scikit-learn`, `pandas`, `jellyfish`를 설치합니다.

## 데이터 준비
`make dir`를 일단 실행한다.

### csv
`data/raw`에 `csv` 파일들을 저장한다.

### PostgreSQL
PostgreSQL 서버를 띄우고, `postgres` 사용자의 비밀번호를 `postgres`로 맞춘다. (`src`의 코드를 직접 수정해도 됨)

`psql postgres postgres`로 PostgreSQL 서버에 접속하고, `create database Kdd2013AuthorPaperIdentification`로 데이터베이스를 생성한다.

`dataRev2.postgres` 파일을 이용해 PostgreSQL 데이터베이스를 구축한다. (`./load-rawdata.sh`)
