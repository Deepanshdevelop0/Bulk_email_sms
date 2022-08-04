# import sounddevice as sd
# from scipy.io.wavfile import write
# import wavio as wv
# import numpy as np
from tkinter import messagebox
import speech_recognition as sr

# freq = 44100

# # def recording
# # for i in range(n):


# arr = np.empty(0)

# duration = 5
# for i in range (1 , duration+1):
#     print(i)
#     if (duration != -1):
#         recording = sd.rec(int (i * freq) , samplerate = freq , channels = 2)
#         arr = np.append(arr , recording)
#         sd.wait()
#         print(arr)


# write("recording4.wav" , freq , arr)

# wv.write("recording5.wav" , arr , freq , sampwidth = 2)



def record():
    
    lang = ""
    lan = input("Enter language to Recognize:")
    languages = ['en-Us' , 'hi-IN']
    if (lan == "English"):
        lang = languages[0]
    elif (lan == "Hindi"):
        lang = languages[1]
    else:
        print("Language not Supported!")
    if (lan == "English" or lan == "Hindi"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print('Clearing background noise..')
                recognizer.adjust_for_ambient_noise(source,duration=1)
                print("waiting for your message...")
                recordedaudio=recognizer.listen(source)
                print('Done recording..!')
                print(recordedaudio)
            try:
                print('Printing the message..')
                text=recognizer.recognize_google(recordedaudio,language = lang)
                print('Your message:{}'.format(text))
                # messagebox.showinfo(title = "Message" , message = text)
                return text
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    i = 1
    while (i != 0):
        # i = int(input("Enter the value: "))
        if (i != 0):
            a = record()
            print(a)
        # messagebox.showinfo(title = "Message" , message = a)
        

