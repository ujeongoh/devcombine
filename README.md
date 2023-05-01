
# 개발 인터넷 강의 사이트 통합 웹 서비스

**기간** : 5/1(월) ~ 5/5(금)
**목표** : 기본적인 개발환경 구축과 간단한 서비스 제작을 통해 파이썬 프로그래밍 기본역량과 Git/Github 사용법 익히기, REST API와 Django 활용
**주제** : 무관(Python, REST API, Django, 데이터 수집 및 가공이 포함된 어떤 주제도 가능함)
**산출물** :
1. 프로젝트 결과물
2. 결과물 코드
3. 프로젝트 보고서(5/12(금) 까지 마감, PPT)
  작성되는 보고서는 전체 공유가 되어 프로젝트 이후 발표회를 가질 계획입니다.

## 📦  Features
* 프로그래머스, 인프런, 패스트캠퍼스, 구름, Udemy (개발강의 한정) 와 같은 인터넷강의 사이트의 강의 데이터 수집 후 사용자에게 통합적인 강의 정보를 제공 
* 사용자가 강의를 찜할 수 있고, 찜한 강의 한번에 볼 수 있다.
* Slack 알림봇을 통해 찜한 강의 알림과 신규 강의 알림 제공

## 🛠️ Tech Stack

`python` `Django`


## ⚙️ Run Locally

프로젝트 클론하기

```bash
  git clone https://github.com/devcombine/devcombine.git
```

프로젝트 폴더로 이동

```bash
  cd devcombine
```

가상환경 폴더 생성 및 활성화

```bash
  python -m venv venv
  source venv/bin/activate
```

환경설정

```bash
  venv/bin/pip install -r requirements.txt
```

