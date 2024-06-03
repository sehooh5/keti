# 개인과제

- 포트폴리오 정리
  - github.io 사용하는게 어떨지?
- 과제내용 총 정리
  - 과제 내용 및 기술들 노션 혹은 velog 등 블로그 형식으로 꾸며보기



### 포트폴리오

- 일정 : 
  - 1.31. ~ 2/2 : 포트폴리오 레퍼런스 찾아보고 어떤 방향으로 나갈지 결정



- chatGPT 가 추천한 요령
  - **관련 자료 수집**: 코드 스니펫, 기술 문서 및 소프트웨어 아키텍처 다이어그램과 같은 작업의 예를 수집합니다.
  - **기술 능력 강조**: 데이터베이스, 서버 측 프레임워크 및 API 개발과 같은 백엔드 기술에 대한 경험을 보여주십시오.
  - **문제 해결 기술 입증**: 복잡한 문제를 해결하고 솔루션을 구현한 방법에 대한 이야기를 공유합니다.
  - **경험 포함**: 직업적 배경과 작업한 관련 프로젝트에 대한 요약을 제공하십시오.
  - **성취 강조**: 당신이 당신의 일에 대해 받은 모든 상, 인증 또는 표창을 강조하십시오.
  - **최신 상태로 유지**: 포트폴리오를 최신 프로젝트와 기술로 정기적으로 업데이트하여 최신 상태로 유지하세요.
  - **단순한 디자인 사용**: 포트폴리오 디자인을 깨끗하고 단순하게 유지하고 콘텐츠에 집중하고 화려한 그래픽으로 독자를 압도하지 마십시오.
  - **직업에 맞게 맞춤화**: 포트폴리오를 지원하는 각 직업의 특정 요구 사항에 맞게 조정하고 가장 관련성이 높은 기술과 경험을 강조하십시오.
  - **평가 포함**: 가능하면 귀하의 능력과 성취를 증명할 수 있는 동료, 관리자 또는 고객의 평가를 포함하십시오



- 정리 : 
  - **프로젝트 수는 2~3개** 





### 코딩테스트

- 매일 1~3개 문제 풀기
- 참고 사이트
  - 프로그래머스 : https://school.programmers.co.kr/learn/challenges?order=recent&page=1
  - LeetCode : https://leetcode.com/problemset/all/



### 과제내용

- 3년의 과정
- 국책 연구과제로 수익성, 수치를 보여줄 수 없다 어떻게 표현할 수 있을까?
- 3년의 과정 외에 따로 했던 프로젝트 사용 가능한 것 잇을지 확인 필요



### 특강 정리

- 포폴
  - 복잡한 로직을 어떻게 풀어냈나 보여줄수 있으면 good - c++ 파이썬연동 풀어내기
  - 피피티로 만들기
    - 이름을 손글씨로 한 사람도 있었다
    - 서비스 내용은 간단하게, 내가 한일 더 자세히
    - 템플릿 - 미리캠퍼스 노트폴리오
    - 상대 배려(면접관) 하는 직관적내용
    - 가독성 직관성



- 자소서

  - 문제 갈등 해결경험
  - **리딩문장**!!! 결과 포함, 항목의 결론 중요
  - 성장과정
  - 강점
  - 지원동기
  - 기업분석!!! 부서 등 상세하게-최초 검색
    - Ex)고도화에 기여하고자~~~

  

- 면접특강

  - 핵심은 내 소개가 아니라 회사에 도움이 될것같은 답변을 해야함
  - 떨어져도 된다는 마인드
  - 말할때 조사 올리기, 0.5배속
  - 내 경험과 jd 를 연관시켜서 말하기, 회사에게 이득되게 답변 만들기!!
  - Ncs.go.kr 직무 필요 확인하기 ,,,직무 기술서 확인



### 개인 일정

#### 1/31

- 개발자 관련 자료 찾기
- 이번주 내로 레퍼런스 및 포폴 정리(주중 시간 이용)



#### 1/31

- 깃허브 정리
- 블로그, 노션 등 어떻게 활용할지
- 이번주 내로 레퍼런스 및 포폴 정리(주중 시간 이용)



#### 2/3

- 국외기술 정리

- 포폴 레퍼 찾기, 진행방향 잡고 주말에도 진행
- 블로그 시작
  - velog : 개발자 친화적
  - tistory : 구글 에드 가능



#### 0206

- 프로그래머스 코딩테스트 시작

  - import 없이 해야함(78.9실패)

    ```py5hon
    # import 를 쓰면 안되는듯 테스트 실패
    import string
    
    alpha = [i for i in string.ascii_lowercase]
    
    def solution(s, skip, index):
        answer = ''
        
        skip_list = list(skip)
        for i in skip:
            alpha.remove(i)
        # 0~21
        for i in s:
            s_index = alpha.index(i)+index
            if s_index >= len(alpha):
                s_index = s_index-len(alpha)
            answer = answer+alpha[s_index]
    
        return answer
    ```

    

  - 78.9% 성공

    ```python
    def solution(s, skip, index):
        answer = ''
        a_num = ord('a')
        z_num = ord('z')
        
        num_list = list(range(a_num, z_num+1))
        s_list = list(s)
        skip_list = list(skip)
        
        for i in skip:
            skip_num = ord(i)
            num_list.remove(skip_num)
            
        nl_len = len(num_list) # index = 0~21
            
        for i in s:
            s_num = ord(i)
            s_index = num_list.index(s_num)+index
            if s_index >= nl_len:
                s_index = s_index - nl_len
            num = num_list[s_index]
            a_chr = chr(num)
            answer = answer+a_chr
    
        return answer
    ```

    

#### 0207

- 블로그 

  - 벨로그, 티스토리 작성 -코딩테스트 쉬운 내용

- 코딩테스트 lv0 계속 풀어나가기

- 최빈값 안됨

  - 오답노트 작성할 것!

  - ```
    def solution(array):
        a_len = len(array)
        a_cnt = {}
        cnt = 0
        dup_cnt = 0
        
        for i in array:
            cnt = 0
            for j in range(0,a_len):
                if i == array[j]:
                    cnt+=1
            
            a_cnt[i]=cnt
        
        max_val = max(a_cnt.values())
        max_key = max(a_cnt, key=a_cnt.get)
        
        for value in a_cnt.values():
            if value == max_val:
                dup_cnt+=1
                
        if dup_cnt >=2:
            return -1      
                    
        return max_key
    ```



#### 0209

- 오답노트 후

- 코딩테스트 진행

  ```
  def solution(sides):
      sum = 0
      max_index = sides.index(max(sides))
      
      for i in range(0,len(sides)):
          if i != max_index:
              sum+=sides[i]
      
      if sum > sides[max_index]:
          return 1
      
      return 2
  ```

- 지식

  - 리스트 내 갯수 세기
    - array.count(n)
  - 문자열은 곱셈이 가능하다
    - string*4 = stringstringstringstring



#### 0210

- 코테 후 포폴준비



#### 0213

- 리서치
  - 포폴 예시 
  - 깃 예시
  - 경력 기술서 
  - 링크드인



#### 0214

- 리서치
  - 포폴 예시 
  - 깃 예시
  - 경력 기술서 
  - 링크드인
- 공고 찾기
  - 카카오 
  - 사람인
  - 자소설



#### 0215

- 그대로 진행
- 클린코드 책 이번주내 끝내기



#### 0216

- 블로그 포스팅 및 코딩테스트

  - ```
    import re
    
    def solution(my_string):
        answer = 0
        numbers = re.findall(r'\d+', my_string)
                
        for num in numbers:
            answer+=int(num)
        return answer
    ```

  - ```
    
    def solution(my_string):
        answer = 0
        temp = ''
        
        for i in my_string:
            if str.isdigit(i):
                temp+=i
            else:
                try:
                    answer+=int(temp)
                    temp = ''
                except:
                    print("temp is empty")
        if temp != '':
            answer+=int(temp)
        return answer
    ```




#### 0217

- 코딩테스트

  - 오답 -> **정답**

    ```python
    
    def solution(keyinput, board):
        answer = [0,0]
        max_ud = (board[1]-1)//2
        max_lr = (board[0]-1)/2
        
        for key in keyinput:
            
            if key == 'up':
                if  max_ud > answer[1] :
                    answer[1]+=1        
            elif key == 'down':
                if  -max_ud < answer[1]:
                    answer[1]-=1
            
            if key == 'right':
                if  max_lr > answer[0]:
                    print('r')
                    answer[0]+=1
            elif key == 'left':
                if -max_lr < answer[0]:
                    print('l')
                    answer[0]-=1
    
        return answer
        
    
    ```

  - **정답**

    ```python
  
    def solution(keyinput, board):
        answer = [0,0]
        max_board_x=(board[0]-1)/2
        max_board_y=(board[1]-1)/2
    
        for i in keyinput:
            if i =="up":
                if max_board_y >= answer[1]+1:
                    answer[1]+=1
            elif i =="down":
                if -max_board_y <= answer[1]-1:
                    answer[1]-=1
            elif i =="right":
                if max_board_x >= answer[0]+1:
                    answer[0]+=1
            elif i=="left":
                if -max_board_x <= answer[0]-1:
                    answer[0]-=1
    
        return answer
    ```



#### 0218

- 17일 위에 내용 오답노트 하기



#### 0220

- 리서치
  - 포폴 예시 
  - 깃 예시
  - 경력 기술서 
  - 링크드인



#### 0221

- 코딩테스트 어렵



#### 0222

- 코딩테스트 오답

- 블로그 작성




#### 0223

- 코딩테스트 0 완료
- 공고 찾기
  - 카카오 
  - 사람인
  - 자소설



#### 0302

- 리서치
  - 포폴 예시 
  - 깃 예시
- 코딩테스트
  - lv1.  카드뭉치



#### 0303

- 리서치
  - 포폴 예시 
  - 깃 예시
- 코딩테스트
  - lv1.  2023 kakao blind - 개인정보 수집 유효기간



#### 0306

- 테스트 본거 정리하는데 줄이는거 생각 다시 해서 줄여서 블로그 올리기
- 내일 대충만든자판 문제 해결하기
- 경력기술서 내용 다시 정리



#### 0307

- 대충만든 자판 블로그 오답노트 작성
- 챗GPT 이용한 서비스 만들어보는 계획



#### 0308

- 챗gpt api 다운로드 및 적용

- 코테

  ```
  def solution(s):
      answer = []
      
      for i in range(len(s)):
          answer.append(0)
  
      for i1, s1 in enumerate(s):
          temp = []
          for i2, s2 in enumerate(s):
              if s1 == s2:
                  temp.append(i2)
                  
          answer[temp[0]] = -1
          for i3, num in enumerate(temp):
              if answer[num] == 0:
                  answer[num] = temp[i3]-temp[i3-1]              
                  
      return answer
  ```

  

#### 0310

- 코테 오답

  - 'baaa'일 경우 해결하기 14일에

  ```python
  def solution(s):
      answer = 0
      # 문제 이해가 어려웠는데 
      cnt = 0
      s_list = []
      
      
      for s1 in s:
          new_s1 = ""
          same = 0
          diff = 0
          cnt = 0
              
          for s2 in s:            
              if s1 == s2:
                  same+=1
                  new_s1+=s2
                  cnt+=1
              else : 
                  diff+=1
                  new_s1+=s2
                  cnt+=1
  
              if same == diff:
                  s = s[cnt:]
                  s_list.append(new_s1)
                  break
              elif len(s) == 1 :
                  s_list.append(s)
                  s = []
                  break
      print(s_list)            
      return len(s_list)
  ```



#### 0314

- 문자열 나누기 진행

  ```
  # 정답
  def solution(s):
      answer = []
      
      # baaa일 경우 
      # s='baaa'
      s2 = ''
      for s1 in s:    
          s2+=s1
          # s2 내에 s2[0]의 개수가 len(s2)//2 과 같을 때 answer에 append
          if s2.count(s2[0]) == len(s2)/2 or len(s) == 1:
              s = s[len(s2):]
              answer.append(s2)
              s2 = ''
          elif len(s2) == len(s):
              s = s[len(s2):]
              answer.append(s2)
              s2 = ''
  
                  
      print(answer)
      return len(answer)
  ```

  

- 포폴 .... !!! 토욜 완성 목표



#### 0316

- git에 잇는 포트폴리오 살려서 페이지 만들기



#### 0317

- 포폴 내용 입력
  - 주소 : https://sehooh5.github.io/ 
  - 자료 : git, google drive, local in mac



#### 0320

-  프로젝트 내용 정리된거 및 내 정보 입력
  - 개발 언어
  - 교육
  - 수상내역



#### 0321

- 프로젝트 세부내용 입력
- git page 업데이트가 안됨
  - 오류 메시지 : Environment URL '' is not a valid http(s) URL, so it will not be shown as a link in the workflow graph.



#### 0424

- 포트폴리오 github io 진행하고 수요일까지 마무리하기
  - 집가서도 무조건 하기!!



#### 0425

- 언어 레벨 표시

  ```html
  <i class="fa fa-square" style="font-size:1rem"></i><i class="fa fa-square" style="font-size:1rem"></i><i class="fa fa-square" style="font-size:1rem"></i><i class="fa fa-square" style="font-size:1rem"></i><i class="fa fa-square-o" style="font-size:1rem"></i>
  ```

  

#### 0426

- 프로그래밍 언어 Docker부분부터 다시 확인 후 시작



#### 0427

- experience 다시 채우기 시작
  - 옆에 리스트 띄워놓고 채우기 
- 3차년도까지 작성 완료(확인 필요)



#### 240306

- 성과 토대로 이력서 수정!



#### 0307

- 책 꼭 읽어보기
  - **코딩 인터뷰 완전 분석** - 면접 준비 전 꼭!
- 링크드인 확인



#### 0311

- 무신사
- 링크드인, 자소설 등등 채용 정리
- 연구계발 계획서 3차년도 정리



#### 0312

- 이지원 사이트 확인작업
  - 협약변경/협약변경신청 -> 변경신청 클릭 -> 검토 -> 닫기
    인력정보 수정 -> "당해년도 참여기간", "당해년도 참여율(A)", 인건비(총액) 확인



#### 0318

- 원티드 킥오프 내일 19일 시작




#### 0328

- 미션1 오늘 마무리하고 제출



#### 0403

- 개인과제 완료 
- 내일 특강



#### 0404

- 특강

- 국내 건설 보안 솔루션 자료 조사 및 기술수준 파악

  - 건설현장 보안 솔루션 : 건설현장의 안전 등을 위해 개발하는 보안 서비스, 시스템 등

      --> edge-cloud 형태의 기술 개발이 필요하다라는 것을 어필



#### 0408

- 건설 보안 솔루션 자료 조사 및 기술수준 파악
  - 외 건설현장 보안 솔루션을 제공하는 몇 가지 주요 기업들은 다음과 같습니다:
    1. **Bosch Building Technologies**: Bosch는 건설 현장을 위한 CCTV 및 보안 시스템을 제공합니다. 그들의 솔루션은 실시간 모니터링, 영상 분석 및 위험 상황 감지를 포함합니다.
    2. **Honeywell**: Honeywell은 건설 현장 보안을 위한 다양한 솔루션을 제공합니다. 이에는 CCTV, 액세스 제어, 화재 감지 및 비상 통신 시스템이 포함될 수 있습니다.
    3. **Axis Communications**: Axis는 네트워크 카메라 및 관련 보안 솔루션을 제공하는 선도적인 기업 중 하나입니다. 그들의 제품은 건설 현장의 영상 감시와 관련된 다양한 요구 사항을 충족시킵니다.
    4. **FLIR Systems**: FLIR은 열화상 카메라 및 관련 솔루션을 제공하여 건설 현장의 보안 및 안전에 기여합니다. 이러한 기술은 주로 야간 모니터링 및 온도 감지에 사용됩니다.
    5. **Avigilon Corporation**: Avigilon은 고해상도 영상 감시 및 분석 솔루션을 제공하여 건설 현장 보안을 강화합니다. 이러한 솔루션은 영상 분석을 통해 위험 상황을 탐지하고 대응하는 데 도움이 됩니다.



#### 0409

- 엣지 문서 작업
  - 설치 부분까지 완료
- 포폴 초안 작업
  - 백엔드 넣어야할 요소 5
    - REST API 개발내용 - CRUD
    - DB 설계
    - github
    - 프로그램 실행 링크 - 없는듯
    - 기술적 하이라이트



#### 0411

- 엣지 문서 작업

  - 설치 이후 app.py 실행내용 설명하면됨

- 동향조사 정리작업

- 포폴 작업

  - 프로필 페이지

  - 프로젝트 페이지

    



#### 0415

- 동향조사 - 지능형 영상보안 시스템 - 국내부분
  - 조사
  - 수준
  - 요약(표)
- 포폴
  - 프로필 페이지
    - 기술 정리
  - 프로젝트 페이지
  - 백엔드 넣어야할 요소 5
    - REST API 개발내용 - CRUD
    - DB 설계
    - github
    - 프로그램 실행 링크 - 없는듯
    - 기술적 하이라이트



#### 0416

- 동향조사 - 지능형 영상보안 시스템 - 국외부분
  - 조사 O
  - 수준 O
  - 요약(표) 
    - axxon 시작하면 됨





#### 0417

- 포폴
  - 프로젝트 페이지
    - **실무 경험 강조 및 구현 사항을 중심으로 직무 역량 상세히 설명** 
    - **직무 수행 외 다양한 기술 스택을 활용한 개발경험으로 열정 피력**
    - **주도적 지식 확장의 근거 제시**



#### 0422

- 포폴 내일까지!
  - 참고 사이트
    - https://zero-base.co.kr/event/media_insight_contents_BE_backend_portfolio_web
    - 경력  :
      - https://www.pptplug.com/class/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&bmode=view&idx=14741319&t=board
      - https://www.rallit.com/hub/resumes/56608/%EC%9C%A4%EC%A2%85%ED%95%84



#### 0423

- 포트폴리오
  - 프로젝트
    - 내용 입력하기
  - 특허 / 기타
    - 초안 짜기



#### 0424

- 프로젝트
  - 4차년도 , 멀캠 내용 입력하기
- 특허 / 기타
  - 초안 짜고 내용 기입



#### 0425

- 프로젝트
  - 요약 내용 정리하고 
  - 세부내용 만들기
- 특허
  - 첫 장 오른쪽 요약내용
  - 다음장 세부내용 사진
- 소프트웨어
  - 오른쪽 요약내용 기입
- 자율개선형과제 연구개발 도식화



#### 0430

- • 경력 사항을 자세히 기술하지 않고 간략하게 서술한 점이 있다. 경력 사항을 더 구체적으로 기술하면 좋을 것이다.

  • 스킬 부분에서 JavaScript, Linux, SQL, HTML, CSS, Oracle Database, MySQL 등의 스킬을 언급하였지만, 이외에도 어떤 스킬을 보유하고 있는지 더 자세히 기술하면 좋을 것이다.

  • 경력 사항과 스킬을 연결하여 어떤 프로젝트에서 어떤 스킬을 활용하였는지 구체적으로 언급하면 좋을 것이다.

- ![image](https://github.com/sehooh5/keti/assets/58541635/83283a67-14db-4398-bee2-f9a5b31534cf)



#### 0502

- 프로젝트

  - 요약 내용 정리하고 
  - 세부내용 만들기

- 특허

  - 첫 장 오른쪽 요약내용
  - 다음장 세부내용 사진

- 소프트웨어

  - 오른쪽 요약내용 기입

  

#### 0507

- 프로젝트
  - 요약 내용 정리하고 
  - 세부내용 만들기
- 특허
  - 첫 장 오른쪽 요약내용
  - 다음장 세부내용 사진
- 소프트웨어
  - 오른쪽 요약내용 기입
- 논문
  - 문제 : 비디오 보안 시스템에서 고화질, 대용량 비디오 데이터 처리의 증가로 인한 서버 과부하가 급증하게 됨.
  - 해결방법 : Docker 컨테이너와 Kubernetes를 활용한 마이크로서비스로 증가된 워크로드를 효율적으로 처리할 수 있는 플랫폼을 사용해 실시간 비디오 스트리밍을 배포할 것을 분산처리를 가능하게함
  - 결과 : CPU 및 메모리 사용량을 최소화하여 시스템 과부하를 완화



#### 0508

- 프로젝트 4차년도 내용 기록
- 특허 세부내용
- 소프트웨어 세부내용
- 무선엣지 과제 사용자 가이드 작성
  - 2차년도 - 사용자 가이드(통합)



#### 0509

- 무선엣지 통합 자료 전달드리기



#### 0514

- 프로젝트
  - 요약 내용 정리하고 
  - 세부내용 만들기
- 특허
  - 첫 장 오른쪽 요약내용
  - 다음장 세부내용 사진
- 소프트웨어
  - 오른쪽 요약내용 기입
- 논문
  - 문제 : 비디오 보안 시스템에서 고화질, 대용량 비디오 데이터 처리의 증가로 인한 서버 과부하가 급증하게 됨.
  - 해결방법 : Docker 컨테이너와 Kubernetes를 활용한 마이크로서비스로 증가된 워크로드를 효율적으로 처리할 수 있는 플랫폼을 사용해 실시간 비디오 스트리밍을 배포할 것을 분산처리를 가능하게함
  - 결과 : CPU 및 메모리 사용량을 최소화하여 시스템 과부하를 완화



#### 0516

- 프로젝트 2 진행중



#### 0521

- 22일 확인
  - https://naver.me/xzcn3kcp 한화 033-330-9789

#### 

#### 0522

- 4년차까지 완료



#### 0528

- 전체 완료
- 피드백 gpt 등 고려해서 수정
  - 이력서 보완
  - 포폴 보완
- 지원시작



#### 0529

- 분원 이사

- 이력서 보완

  • 경력 사항을 자세히 기술하지 않고 간략하게 서술한 점이 있다. 경력 사항을 더 구체적으로 기술하면 좋을 것이다.

  • 스킬 부분에서 JavaScript, Linux, SQL, HTML, CSS, Oracle Database, MySQL 등의 스킬을 언급하였지만, 이외에도 어떤 스킬을 보유하고 있는지 더 자세히 기술하면 좋을 것이다.

  • 경력 사항과 스킬을 연결하여 어떤 프로젝트에서 어떤 스킬을 활용하였는지 구체적으로 언급하면 좋을 것이다.

- 포폴 보완



#### 0530

- 지원 시작
- 조건 좋아지더라도 계속



#### 0603

- 물타기 계산기 
  - 보유 수량 * 매입가격
  - 보유 수량 * 현재가격
  - 수익률
  - 목표 수익률 입력
  - 필요 매수 수량 * 현재가격