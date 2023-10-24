import openai
import pyttsx3
import speech_recognition as sr
import speech_recognition as sr
import pywhatkit
import random


# Set Openai's API's Key

openai.api_key = "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"



# initialize the text to speach engine

engine = pyttsx3.init()

# change engine speach rate

engine.setProperty('rate', 180)

voice = engine.getProperty('voices')

# get available voicess

engine.setProperty('voice', voice[1].id)

# counter just for the interacting purposes

interaction_counter = 0


def transcribe_audio_to_text(filename): 
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

    try:
        # using google speech recognition
        return recognizer.recognize_google(audio)
    except:
        print("")

def run_alexa():
    command = conversation()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        speak_text('playing ' + song)
        pywhatkit.playonyt(song)
        

def ChatGpt_conversation(conversation):
    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation
    )
    
    api_usage = reponse['usage']
    print('Total token consumes: {0}'.format(api_usage['total_tokens']))
    conversation.append({'role': reponse.choices[0].message.role, 'content': reponse.choices[0].message.content })
    return conversation

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    


# starting conversation

conversation = []
conversation.append({'role': 'user', 'content': 'Please act like Appel voice assistance siri and be natural'})
conversation = ChatGpt_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())



def activate_assistant():
    starting_chat_phrases = [
        " Yes sir, how can i help",
        " alright i get it , give me a minute",
        " sure sir, i am here to help",
        " okay give me a minute",
        " yes sir, i am here to help",
        " Jarvis here, i'm on it"
    ]
    
    continue_chat_phrases = ["yes","alright","i'm on it","yes boss","i'm all ears"]
    random_chat = ""
    
    if(interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    
    else:
        random_chat = random.choice(continue_chat_phrases)
        
    return random_chat

def append_to_log(text):
    with open('chat_log.txt','a') as f:
        f.write(text + "\n" )
        

while True:
    # wai for user to say Jarvis
    print("Listening... say 'alexa' ")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source) 
        try:
            transcription = recognizer.recognize_google(audio)
            if "alexa" in transcription.lower():
                interaction_counter +=1
                
                # activate assistant and record audio
                filename = "input.wav"
                
                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)
                recognizer =  sr.Recognizer()   
                
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit= None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                
                text = transcribe_audio_to_text(filename)
                
                if text: 
                    print(f"You said: {text}")
                    append_to_log(f"You: {text}\n")
                    
                    #generate reponse using ChatGpt
                    
                    print(f"alexa says: {conversation}")
                    
                    prompt = text
                    
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGpt_conversation(conversation)
                    
                    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content']))
                    append_to_log(f"Jarvis: {conversation[-1]['content'].strip()}\n")
                    
                     
                     # read response with using text to speech
                     
                    speak_text(conversation[-1]['content'].strip())
                    
                   
        except Exception as e:
            continue
            # print(" an Error occured: {}".format(e))