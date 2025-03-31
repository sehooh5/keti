

db에 대한 설명을 드릴건데요. 주요 테이블 순서대로 관련된 관계테이블 함께 설명하면서 넘어가겠습니다.



### 1. **User 테이블**

- 서비스 핵심 테이블중 하나인 User 테이블입니다.

- 사용자의 정보 (이름, 닉네임, 프로필 이미지, 생년월일, 성별, 직업 등)를 담고 있고

- 약관 및 마케팅 동의 여부를 저장합니다.

- 그리고, 사용자 활동을 추적하기 위한 `followers_count`, `followings_count`, `posts_count` 

  등의 통계 필드도 포함되어 있습니다. 

- 기본적으로 중복 방지를 위해 **다다대 관계 테이블**은 PK, FK 설정을 해두었는데요,

  - **user_follow_table** 은 유저 간의 다대다 자기참조 관계입니다.
  - `follower_id`, `following_id`가 복합키로 설정되어있습니다.



#### UserAuthInfo

- UserAuthInfo 유저 인증 테이블입니다.
- 쇼빌리티는 3가지 방법의 가입이 가능하며 이메일, 카카오, 애플 아이디로 가입이 가능합니다.
- 그에 대한 세가지 컬럼이 있구요, 중복적으로 인증이 가능합니다.
- 사용자 아이디 user_id를 FK 포린키로 갖고있습니다.

------

### 2. **Post (게시물)**

- 다음은 `Post` 테이블입니다. 
- 포린키가 2개인데 작성자 아이디(`author_id`) 가 있고
- 게시물 당 1개의 카테고리를 갖고 잇어, 카테고리 아이디(`category_id`)가 있습니다.
- 프로젝트 내 모든 삭제는 Soft delete를 하려고 하고있고, 그에 필요한 `is_deleted` 필드가 있습니다.
  - 관계 테이블로는 유저가 좋아요를 누른 게시물을 관리하는 **user_post_table** 다대다 테이블이 있습니다.
- 하나의 게시물은 여러 개의 이미지를 (`PostImage`) 가질 수 있고

### 4. **PostImage**

- 게시물의 이미지인 PostImage를 따로 테이블로 정의했습니다. 
- 게시물의 이미지 정보를 저장하고,
- `post_id`를 FK로 가지고 있으며,
- 하나의 게시물에 여러 이미지가 있어서 `order`컬럼을 통해 이미지 순서를 관리합니다.

------

### 3. **Category / Tag**

- 다음은 기본적으로 쇼빌리티 프로젝트에 하드하게 설정된 카테고리 태그입니다.
- `Category`는 게시물을 대분류하는 카테고리 테이블이고,
  - user는 여러개의 관심 카테고리를 가입 시 혹은 프로필 변경에서 선택할 수 있습니다.
  - 유저가 선호하는 카테고리 정보를 저장하는 다대다 테이블 **user_preferred_categories_table**로 관리합니다
- `Tag`: 다음은 카테고리에 속하는 소분류인  태그입니다.
  - 태그는 기본적으로 하드하게 입력된 태그가 있고, 사용자가 자율적으로 게시물 등록 시 추가할 수 있습니다.
    - 하드하게 입력된 태그는 분류가 나누어 져있으며, 분야/ 스타일 으로 나누어 관리하고 있습니다.
  - 카테고리와 태그는 다대다관계이며,  **category_tag_table**을 통해 연결됩니다.
- 게시물에 여러개의 태그를 선택할 수 있어, **post_tag_table**을 통해 관리합니다.

------

### 5. **댓글 (Comment)**

- 다음은  댓글이며 Comment 테이블입니다

-  작성자 아이디(`user_id`)와 게시물 아이디(`post_id`)를 FK로 가집니다.

- 부모댓글아이디로 자기참조를 해 FK를 갖고 있습니다.

- `depth` 필드를 통해 대댓글 구조를 관리할 수 있도록 설계되어 있습니다.

  - 유저가 댓글에 좋아요를 누른 정보를 저장하는 다대다관계 테이블 **user_liked_comments_table**입니다,

  

이상 프로젝트의 DB 구조에 대해서 설명을 마치겠습니다. 질문 있으시면 지금이든 언제든 질문 주시고, 수정 개선이 필요한점이 있으면 언제든 말해주시고 같이 고쳐나가면 될 것 같습니다.



테이블 명 정리, 테이블 -> 도메인에 넣기, 컬럼명 자세하기 넣기

타입체크 살리기 -> 에러 안나게 살려보기

Pipenv run typecheck

> 해당 자료는 kamranahmedse의 developer-roadmap 중 backend(https://roadmap.sh/backend)을 토대로 백엔드의 기초를 제안합니다.

[해보기]

데이터 베이스 심화, RestAPI, layer architecture(https://kimkani.tistory.com/59)

백엔드 로드맵 : https://github.com/Han-Kyeol/developer-roadmap-kr-





## 게시글 목록 조회 API

### method : `GET`

### url : `/posts/`

### Request

- **header**
  - `X-Auth-Token`: `string` (로그인 유저 인증 토큰, 필수X)
- **query parameter**
  - `skip`: `int` (기본값: 0)
  - `limit`: `int` (기본값: 10)
- **body**
  - 없음

### Response (성공시)

- **http status**

  - `200 OK`

- **body**

  ```
  json
  
  
  복사편집
  [
    {
      "id": 4,
      "title": "test3",
      "description": "test3",
      "createdAt": "2025-03-24T14:45:59.574816Z"
    },
    {
      "id": 3,
      "title": "test1",
      "description": "test1",
      "createdAt": "2025-03-24T14:44:23.166480Z"
    },
    {
      "id": 2,
      "title": "test2",
      "description": "test2",
      "createdAt": "2025-03-24T14:43:45.031022Z"
    },
    {
      "id": 1,
      "title": "test",
      "description": "test",
      "createdAt": "2025-03-24T14:42:56.828226Z"
    }
  ]
  ```

------

## 게시글 생성 API

### method : `POST`

### url : `/posts/`

### Request

- **header**
  - `X-Auth-Token`: `string` (로그인 유저의 인증 토큰)
- **query parameter**
  - 없음
- **body**
  - **형식**: `multipart/form-data` (이후 image 파일 업로드 시 form 으로 입력 필요)
  - **내용**
    - `title`: `string` (필수)
    - `description`: `string` (필수)
    - `category_id`: `int` (필수)
    - *(향후 추가 예정)*
      - `tags`: `List[string]`
      - `images`: `List[UploadFile]` (1개 이상 필수)

### Response (성공시)

- **http status**

  - `201 Created`

- **body**

  ```
  null
  ```



