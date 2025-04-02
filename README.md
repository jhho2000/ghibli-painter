# 지브리 스타일 이미지 생성기 (Ghibli Painter)

사용자가 업로드한 이미지를 스튜디오 지브리 스타일의 애니메이션 이미지로 변환해주는 웹 애플리케이션입니다.

## 주요 기능

- 사용자 이미지 업로드
- OpenAI GPT-4o-mini를 사용한 이미지 상세 묘사
- Google Gemini를 활용한 지브리 스타일 이미지 생성
- 원본 이미지와 생성된 이미지 비교 기능

## 기술 스택

- **백엔드**: Flask (Python)
- **프론트엔드**: HTML, CSS, JavaScript
- **API**:
  - OpenAI API (이미지 묘사)
  - Google Generative AI (Gemini, 이미지 생성)

## 설치 방법

1. 저장소 클론
   ```
   git clone [저장소 URL]
   cd ghibli-painter
   ```

2. 가상환경 생성 및 활성화
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 필요한 패키지 설치
   ```
   pip install -r requirements.txt
   ```

4. 환경 변수 설정
   - `.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 내용 추가:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## 실행 방법

1. Flask 애플리케이션 실행
   ```
   python app.py
   ```

2. 웹 브라우저에서 접속
   ```
   http://localhost:5000
   ```

## 사용 방법

1. '이미지 선택하기' 버튼을 클릭하여 변환하고 싶은 이미지를 업로드합니다.
2. '지브리 스타일로 변환하기' 버튼을 클릭합니다.
3. 잠시 기다리면 AI가 이미지를 분석하고 지브리 스타일로 변환된 이미지를 생성합니다.
4. 원본 이미지와 생성된 이미지를 비교해볼 수 있습니다.
5. 이미지에 대한 AI의 상세 묘사도 함께 확인할 수 있습니다.

## 작동 원리

1. 사용자가 업로드한 이미지를 OpenAI의 GPT-4o-mini 모델에 전송하여 이미지에 대한 상세한 묘사를 생성합니다.
2. 생성된 묘사를 바탕으로 Google Gemini 모델에 지브리 스타일의 이미지 생성을 요청합니다.
3. 생성된 이미지와 원본 이미지, 그리고 이미지 묘사를 사용자에게 표시합니다.

## 주의사항

- 이 애플리케이션을 사용하기 위해서는 유효한 OpenAI API 키와 Google API 키가 필요합니다.
- 이미지 생성에는 시간이 소요될 수 있으며, API 사용량에 따라 비용이 발생할 수 있습니다.
- 생성된 이미지는 AI에 의해 만들어진 것으로, 완벽한 지브리 스타일을 보장하지 않습니다.

## 라이센스

[라이센스 정보 추가]
