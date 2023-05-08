from emotion_detect import *
import re
import time
import chatgpt
from chatgpt import generate_gpt3_response


if __name__ == "__main__":
    DEBUGGING = True
    
    chatgpt.conversation[0]['content'] = re.sub(r'\s+', ' ', chatgpt.conversation[0]['content'].strip())
    EMOTIONS = ['당황', '분노', '불안', '슬픔', '중립', '행복', '혐오']
    
    # example Emotion Classifier
    while True:
        sen = input("텍스트 입력 > ")
        if sen in ['Q', 'q']:
            print("BYE !")
            break
        
        start = time.time()
        emotion_pred = emotion_classifier.predict(sen)
        print(emotion_pred)
        end = time.time()
        
        if DEBUGGING:
            print(f"prediction time : {end - start:.5f} sec\n")
        
        # ###################################################
        # # 감정 분류를 이용한 gpt 활용 EXMPLE #1 - rule based
        # if emotion_pred[0] in ['분노', '불안', '슬픔', '혐오']:
        #     sen = '공감해 줘. 조언해 줘. ' + sen
        # else:
        #     sen = '공감해 줘. ' +  sen
        # ###################################################
        
        ###################################################
        # 감정 분류를 이용한 gpt 활용 EXMPLE #2 - prompt with rule based
        if emotion_pred[0] in ['분노', '불안', '슬픔', '혐오']:
            sen = '공감해 줘. 조언해 줘. ' + sen
        else:
            sen = '공감해 줘. ' +  sen
        ###################################################
            
        start = time.time()
        print(generate_gpt3_response(chatgpt.conversation, sen))
        end = time.time()
        if DEBUGGING:
            print(f"gerenating time : {end - start:.5f} sec\n")
