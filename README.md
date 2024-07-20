## 프로젝트 구성
  infra/
      dev/
          app/
          nginx/
          uwsgi/
      prod/
  photocard_market/
      account/
      buy/
      config/
      product/
      sale/
  manage.py
  docker-compose-dev.yaml

- **infra**:
  - 운영 환경(dev, prod)별로 구성되며, 각각 `app`, `nginx`, `uwsgi` 디렉토리로 나뉘어 필요한 파일을 포함합니다.
  - 최상단 폴더의 `docker-compose-{환경}.yaml` 파일을 사용하여 설정됩니다.

- **photocard_market**:
  - Django의 프로젝트 및 앱 구조를 따릅니다.
  - `startapp` 또는 `startproject`로 생성된 디렉토리 구조입니다.
  - 코드 컨벤션은 `black`, `isort` 패키지를 사용하여 통일화되어 있습니다.
  - 기본적으로 해당 프로젝트는 아래와 같은 기획을 기준으로 작성되었습니다.
    1. 관리자는 인증된 포토카드를 앱에 등록합니다.
    2. 인증된 포토카드는 앱 내에서 판매가 가능합니다.
    3. 판매자는 포토카드를 조회하여 판매 신청을 합니다.
    4. 구매자는 판매 목록에 올라온 포토카드를 구매합니다.
  - `추후 개선점`
    1. 구매자도 구매 신청을 통해 포토카드를 구매가능
    2. 현재 1개만 등록 및 판매 -> 여러 장 등록 및 판매, 구매도 가능

- **DB**:
<img width="599" alt="DB TABLE" src="https://github.com/user-attachments/assets/1dbef145-0142-4198-a7c1-0ada2994a8f5">

## 프로젝트 설명

- **account**:
  - 회원 가입, 로그인 API
  - email 기반으로 등록합니다.
  - JWT 토큰은 로그인 시 생성되며, cookie를 통해 전달됩니다.

- **buy**:
  - 구매에 대한 조회, 등록, 수정 API
  - 구매 API는 로그인 후 접근할 수 있습니다.

- **product**:
  - 제품에 대한 등록/검색 API
  - 등록은 admin(관리자)만이 할 수 있습니다.
  - 프로젝트 내에서 구매/판매하기 위해서는 관리자가 제품을 먼저 등록해주어야 합니다.
  - 검색은 모든 사용자가 가능합니다.

- **sale**
  - 판매에 대한 조회, 등록, 수정 API
  - 판매 조회(detail/list) API는 모두 접근할 수 있습니다.
  - 판매 조회를 제외한 API는 로그인 후 가능합니다.

- **admin**:
  - 각 app 별로 admin 기능을 추가했습니다. - {app_name}/admin.py
  - admin 계정은 db migration 시 signals.py를 통해 자동 생성됩니다. - account/signals.py

## API 리스트
프로젝트 내 API들은 Swagger(<http://127.0.0.1/swagger>)를 통해 확인할 수 있습니다.

  접근 상태  METHOD       PATH                    DESCRIPTION
- 모든 유저   POST  account/register                회원 가입
- 모든 유저   POST  account/login                   로그인    

- 인증 유저   GET   photocard/buy/list              유저가 구매중인 or 구매한 포토카드 목록 조회
- 인증 유저   PUT   photocard/buy/register/{id}     포토카드 구매 신청
- 인증 유저   PUT   photocard/buy/end/{id}          포토카드 구매 확정
- 인증 유저   PUT   photocard/buy/cancel/{id}       포토카드 구매 취소

- 모든 유저   GET   photocard/sale/list             앱에서 판매중인 포토카드 목록 조회
- 모든 유저   GET   photocard/sale/{id}             포토카드 상세 조회
- 인증 유저   POST  photocard/sale/register/{id}    포토카드 판매 신청
- 인증 유저   PUT   photocard/sale/change/{id}      포토카드 판매 가격 변경

- 모든 유저   GET   product/photocard/list          등록된 포토카드 목록 조회
- 모든 유저   GET   product/photocard/search?name=  포토카드 검색

## 프로젝트 실행 방법

1. 기본적으로 Docker Compose를 사용하여 프로젝트를 실행합니다.
   - 최상단 폴더에 있는 `docker-compose-{환경}.yaml` 파일을 기반으로 설정됩니다.
   - 운영 환경(prod)에서는 settings에 있는 변수들을 `.env` 파일로 분리하거나 AWS Secret Manager를 활용하여 구성합니다.

2. 프로젝트를 git clone한 후, Compose 파일이 있는 폴더로 이동하여 아래 명령어를 실행합니다:
   ```sh
   docker compose -f docker-compose-dev.yaml up -d
   
3. 만약 Docker를 사용하지 않고 직접 프로젝트를 실행하려면, 아래 명령어를 통해 환경을 셋팅합니다.
    ```sh
    poetry shell && poetry install --no-root
    python manage.py makemigrations && python manage.py migrate
  
4. 테스트 코드는 각 app 폴더 내 `tests.py` 에 있으며, 
    총 4가지의 테스트를 추가했습니다. 추후 추가될 예정입니다.

    - account
      test_user_login           : 로그인 테스트
      test_user_login_invalid   : 비밀번호 검증 테스트

    - sale
      test_sale_register        : 판매 등록 테스트
      test_sale_price_change    : 판매 가격 수정 테스트

    해당 테스트는 아래 명령어를 통해 진행할 수 있습니다.
    ```sh
    python manage.py test "app_name" --settings=config.settings.base

# 저작권 및 사용권 정보
해당 프로젝트는 과제용으로 작성되었으며, 과제 심사가 끝난 후 삭제될 예정입니다.

# 버전 및 업데이트 정보
Python 버전: 3.10
Django 버전: 4.2
DB: MySQL 8.0
그 외 패키지 버전은 requirements.txt에서 확인할 수 있습니다.