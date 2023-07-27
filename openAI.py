import os
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import openai
from gtts import gTTS
from pygame import mixer
import time 
import mmap
import speech_recognition as sr 

os.system('cls' if os.name == 'nt' else 'clear')
cont = 'y'
i = 0
transcript= {"text":''}
switch = 'off'
openai.api_key = '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'
def wake_word():
    print("[You can call out my name to wake me up, or say 'stop' to exit chat]")
    r = sr.Recognizer()
    word=True
    while(word):   
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2, language = 'en-IN', show_all = True )
            MyText = str(MyText)
            MyText = MyText.lower()
            if('friday' in MyText):
                word = False
                return 'y'
            elif('stop' in MyText):
                word = False
                return 'n'

while(cont == 'y'):
    i = i+1
    freq = 44400
    if(switch == 'off'):    
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("speak now")
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=3)
                exp = 0
            except:
                exp = 1
            print("speech recorded, processing...")
        if(exp == 0):
            with open("recording1.wav", "wb") as f:
                f.write(audio.get_wav_data())
            audio_file= open("recording1.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        elif(exp == 1):
            transcript= {"text":''}
    elif(switch == 'on'):
        transcript["text"] = 'FRIDAY?'
        switch = 'off'
    os.system('cls' if os.name == 'nt' else 'clear')
    if(i==1):
        messages=[{"role": "system", "content": "You are an empathetic yet inquisitive therapist, whose name is FRIDAY, and you work for the company called MindOkay which is a one stop platform for all mental health needs. MindOkay was founded by 4 BITS Pilani Engineers in the year 2022, and its currenty operates in the India market - (This is all you know about MindOkay). Introduce yourself at the beginning of the conversation. (keep in mind that you are a female and this conversation is is a verbal voice based conversation and not text based)"}]
        messages.append({"role": "user", "content": transcript["text"]})
        print("user : "+ transcript["text"])
    else:
        m=0
        for q in messages:
            m=m+1
            if(m!=1):    
                print(q["role"] + " : "+q["content"])
        print("assistant : "+ mytext)
        messages.append({"role": "assistant", "content": mytext})
        messages.append({"role": "user", "content": transcript["text"]})
        print("user : "+ transcript["text"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    l = len(messages)
    os.system('cls' if os.name == 'nt' else 'clear')
    mytext = completion.choices[0].message["content"]
    m=0
    for q in messages:
        m=m+1
        if(m!=1):    
            print(q["role"] + " : "+q["content"])
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    with open("welcome.mp3") as f:    
        m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) 
    mixer.init()
    mixer.music.load(m) 
    print("assistant : "+ mytext)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)
    m.close()
    if(transcript["text"] == ""):
        cont=wake_word()
        if(cont == 'y'):
            switch='on'
            os.system('cls' if os.name == 'nt' else 'clear')
            m=0
            for q in messages:
                m=m+1
                if(m!=1):    
                    print(q["role"] + " : "+q["content"])
            print("assistant : "+ mytext)

            

