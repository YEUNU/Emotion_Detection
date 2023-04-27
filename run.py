from emotion_detect import *
import time

if __name__ == "__main__":
    # example Emotion Classifier
    while True:
        sen = input("텍스트 입력 > ")
        if sen in ['Q', 'q']:
            print("BYE !")
            break
        
        start = time.time()
        print(emotion_classifier.predict(sen))
        end = time.time()
        print(f"prediction time : {end - start:.5f} sec\n")