import os
import openai
openai.organization = "org-URZ05Egxb2USeXMQiHVKMCKr"
openai.api_key = "open api key" # 공급 받아야함


# conversation=[] # 대화 내용

# conversation.append({"role":"system", "content":"""

#     공감을 원한다면 최대한 감정적으로 공감해 주세요.
#     예를 들어 상대방의 메세지에 '공감해 줘.'같은 말이 포함 되었다면
#     감정적인 위로를 하도록 합니다.
    
#     다른 예로 상대방의 메세지에 '조언해 줘.'같은 말이 되었다면
#     실질적인 조언을 하도록 합니다.
    
#     상대방의 기분이 부정적이면 공감과 조언을 같이 하도록 합니다.
#     예를 들어 상대방의 메세지가 '지금은 말할 기분이 아니네.' 라면
#     감정적인 위로와 도움이 되는 조언을 하도록 합니다.
    
#     상대방의 기분이 긍정적이면 공감을 하도록 합니다.
#     예를 들어 상대방의 메세지가 '오늘 시험에 합격했어.' 라면
#     '와, 합격이라니! 노력한 만큼의 보람이 있군요.' 와 같은
#     감정적인 응답을 하도록 합니다.
    
#     만약 이야기 화제가 전환 된다면 최근의 화제와의 관련성을 고려해
#     적절한 응답을 하도록 합니다.
#     """}) # 초기 요청


# 조언 역할을 하는 함수
def generate_gpt3_response(conversation, user_text, print_output=False):
    conversation.append({'role':'user', 'content': user_text}) # 사용자의 메세지 저장
    
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #prompt=user_text, # What the users typed in
        temperature=0, # Level of creativity in the response. 응답 창의력 레벨
        #max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        messages=conversation, # 대화 흐름 파악
        # messages=[
        #     {"role":"system", "content": "문장에서 감정을 캐치해."}, # 전반적 모델 흐름 부여
        #     {"role":"user", "content":user_text}, # 직접 전달하는 사용자 메세지
        # ],
        stop=["\n"] # An optional setting to control response generation
    )
    
    # print(completions)
    
    conversation.append({'role':completions['choices'][0]['message']['role'],'content':completions['choices'][0]['message']['content']})
    # 챗봇의 응답 저장
    
    return completions.choices[0]['message']['content']


# generate_gpt3_response() # 터보 모델에게 전달할 메세지 스트링
