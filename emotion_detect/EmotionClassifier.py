import os
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

import pandas as pd
pd.options.display.max_columns = None
import numpy as np

import torch
from transformers import AutoModel, AutoTokenizer

class Bert(torch.nn.Module):
    def __init__(self, bert_pretrained, dropout_rate=0.5, n_classes=7):
        super(Bert, self).__init__()
        self.bert = AutoModel.from_pretrained(bert_pretrained)
        self.dr = torch.nn.Dropout(p=dropout_rate)
        self.fc = torch.nn.Linear(768, n_classes)
    
    def forward(self, input_ids, attention_mask, token_type_ids):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        last_hidden_state = output['last_hidden_state']
        x = self.dr(last_hidden_state[:, 0, :])
        x = self.fc(x)
        return x


class EmotionClassifier():
    def __init__(self, device, model, tokenizer, labels_dict, max_length=64):
        self.device = device
        model.to(self.device)
        self.model = model
        self.tokenizer = tokenizer
        self.labels = labels_dict
        
    def predict(self, sentence):
        tokens = self.tokenizer(
            sentence,                # 1개 문장 
            return_tensors='pt',     # 텐서로 반환
            truncation=True,         # 잘라내기 적용
            padding='max_length',    # 패딩 적용
            add_special_tokens=True, # 스페셜 토큰 적용
            max_length = 64,
        )
        tokens.to(self.device)
        prediction = self.model(**tokens)
        prediction = torch.nn.functional.softmax(prediction, dim=1)
        output = prediction.argmax(dim=1).item()
        prob, result = prediction.max(dim=1)[0].item(), self.labels[output]
        # print(f'[{result}]\n확률은: {prob*100:.3f}% 입니다.')
        
        return result, prob
        
if __name__ == "__main__":
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    print(device)
    
    N_CLASSES = 7
    LABEL_DICT = {idx : label for idx, label in zip(range(N_CLASSES), ['anger', 'disgust', 'fear', 'happiness', 'neutralism', 'sadness', 'surprise'])}
    
    CHECKPOINT_BASE = "klue/bert-base"
    PRETRAINED = "/home/wonhong/workspace/Emotion_Detection/DL/models/clean_norm_repeat/klue-bert-token_len_64-batch_size_16-drop_out_0.5-lr_2e-05-weight_decay_0.01 + 1_best.pth"

    token_len = 64
    drop_out = 0.5
    
    model = Bert(CHECKPOINT_BASE, drop_out, N_CLASSES)
    model.load_state_dict(torch.load(PRETRAINED))
    eclf = EmotionClassifier(device, model, AutoTokenizer.from_pretrained(CHECKPOINT_BASE), LABEL_DICT, max_length=token_len)
    
    # dummy prediction for gpu warming up, It would take about 5~ sec.
    eclf.predict("warm up") 
    
    import time
    while True :
        sentence = input("Enter txt :")
        if sentence == 'q' or sentence == 'Q':
            print("BYE")
            break
        start = time.time()
        print(eclf.predict(sentence))
        end = time.time()
        print(f"time to predict : {end-start:.5f} sec")