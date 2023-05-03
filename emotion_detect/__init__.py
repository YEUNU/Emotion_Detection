from .EmotionClassifier import *
import os

if torch.cuda.is_available():
    device = torch.device('cuda:0')
else:
    device = torch.device('cpu')
print(device)

N_CLASSES = 7
# LABEL_DICT = {idx : label for idx, label in zip(range(N_CLASSES), ['anger', 'disgust', 'fear', 'happiness', 'neutralism', 'sadness', 'surprise'])}
LABEL_DICT = {idx : label for idx, label in zip(range(N_CLASSES), ['당황', '분노', '불안', '슬픔', '중립', '행복', '혐오'])}

# base model name
CHECKPOINT_BASE = "klue/bert-base"
# fine-tuned model path
exe_dir = os.getcwd()
dest_path = os.path.join(exe_dir,"emotion_detect","multi-datasetklue-bert-token_len_64-batch_size_16-drop_out_0.5-lr_2e-05-weight_decay_0.01 + 9.pth")

PRETRAINED = dest_path

# model params
TOKEN_LEN = 64
DROP_OUT = 0.5

# warm up
model = Bert(CHECKPOINT_BASE, DROP_OUT, N_CLASSES)

model.load_state_dict(torch.load(PRETRAINED,map_location=device))
model.to(device)
emotion_classifier = EmotionClassifier(device, model, AutoTokenizer.from_pretrained(CHECKPOINT_BASE), LABEL_DICT, max_length=TOKEN_LEN)


# DUMMY PREDICTION for GPU warming up, It would take a few sec.
emotion_classifier.predict("warm up")