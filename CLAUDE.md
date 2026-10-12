# 프로젝트 개요

## 파일 구조
-.env:ANTHROPIC_API_KEY보관
-data.json:기록이저장되는파일
-ai_helper.py:Cluade API를사용하는 ask_ai()함수 정의 
-PLAN.md:프로젝트기획서

## 규칙
-항상PLAN.md기획서를 기준으로 구현할것
-API 호출은 반드시ask_ai()함수를 거칠것
-API KEY는 .env에서 읽고코드에 직접쓰지말것
-기록은 data.json에서리스트 내부  딕셔너리로 한 개씩 저장
-파일이 없거나 비어있을 때는 빈 목록으로 시작하도록 구현
