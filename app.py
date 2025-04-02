import os
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
# import google.generativeai as genai
# import google.generativeai.types as types
from google import genai
from google.genai import types

import requests
from PIL import Image
from io import BytesIO

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    # 업로드된 이미지 처리
    image = request.files['image']
    image_base64 = base64.b64encode(image.read()).decode('utf-8')

    describe_photo_prompt = """
    You are a visual storytelling and scene description expert with deep knowledge in photography, art, and narrative analysis.
    Your task is to vividly describe every essential visual element in the photo I provide. The goal is to help someone who cannot see the image fully understand it.
    Start by describing the main subject of the image. Include details such as their appearance, clothing, facial expressions, body posture, and any actions they are performing.
    Then, describe the background setting. Mention elements such as location, architecture, landscape, weather, lighting, and time of day if possible.
    Next, identify any important objects or symbols in the scene. Point out their position, relevance, or potential meaning.
    After that, explain the overall atmosphere and emotional tone conveyed by the photo. Consider how the composition, lighting, color palette, and expressions contribute to the mood.
    Finally, infer what story or narrative might be suggested by the image. Imagine what could have happened just before or what might happen next, based on visual clues.
    Keep your description vivid, immersive, and full of rich detail. Use precise and evocative language, as if painting the scene with words.
    Take a deep breath and let’s work this out in a step by step way to be sure we have the right answer.
        """;

    try:
        # ChatGPT API를 통해 이미지 묘사 요청
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": describe_photo_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ],
            max_tokens=300
        )
        
        description = response.choices[0].message.content

        # Gemini로 이미지 생성
        ghibli_image_prompt = f"""
        You are a professional illustrator specialized in Studio Ghibli-style artwork. Please redraw the following scene as if it were a frame from a Studio Ghibli animation:
        {description}
        Maintain the original composition and elements, but transform everything into the hand-drawn, whimsical, and nostalgic visual style seen in Hayao Miyazaki's films. Use soft lighting, painterly textures, warm pastel colors, and a magical, storybook-like atmosphere. No realistic photo details – everything should feel animated, peaceful, and full of quiet emotion.
        """
        
        # 이미지 생성
        model = "gemini-2.0-flash-exp-image-generation"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=ghibli_image_prompt),
                ],
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "image",
                "text",
            ],
            response_mime_type="text/plain",
        )
        
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        


        # print(response)

        # 이미지 URL 추출
        generated_image_url = "이미지 생성에 실패했습니다."
        
        try:
            # 응답 구조 확인
            if hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    # inline_data가 있는 경우 (이미지 데이터)
                    if hasattr(part, 'inline_data') and part.inline_data:
                        encoded_image = base64.b64encode(part.inline_data.data).decode('utf-8')
                        generated_image_url = f"data:{part.inline_data.mime_type};base64,{encoded_image}"
                        break
                    # text가 있는 경우 (텍스트 응답)
                    elif hasattr(part, 'text') and part.text:
                        # 텍스트가 JSON 형식인 경우 처리
                        text_content = part.text
                        print(f"텍스트 응답: {text_content}")
                        # 여기서는 텍스트 응답을 그대로 반환
                        generated_image_url = text_content
                        break
        except Exception as extract_error:
            print(f"이미지 URL 추출 오류: {str(extract_error)}")

        return jsonify({
            'description': description,
            'image_url': generated_image_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
