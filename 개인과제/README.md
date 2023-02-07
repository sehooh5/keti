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



#### 0208

