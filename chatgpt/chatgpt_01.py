import os
import openai
openai.organization = "org-URZ05Egxb2USeXMQiHVKMCKr"
openai.api_key = "" # chatgpt api 

# 조언 역할을 하는 함수
def generate_gpt3_response(user_text, print_output=False):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #prompt=user_text, # What the users typed in
        temperature=0, # Level of creativity in the response. 응답 창의력 레벨
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        messages=[
            {"role":"system", "content": "넌 조언해 주면 돼."}, # 메세지로 챗봇에게 역할 부여
            {"role":"user", "content":user_text}, # 직접 전달하는 사용자 메세지
        ],
        stop=["."] # An optional setting to control response generation
    )
    
    #print(completions)
    
    return completions.choices[0]['message']['content'] # stop, max_tokens로 출력 형식 조정 가능

# generate_gpt3_response('신라면') # 터보 모델에게 전달할 메세지 스트링
