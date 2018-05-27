from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import speech_recognition as sr
#read_only will make sure that bot doesn't learn anything new on it's own
bot = ChatBot('Bot',read_only=True,
              logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer')

while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            #will remove noise which comes when microphone is used
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            message = r.recognize_google(audio)
            print("You said: " + message)
            
            if message.strip().lower() != 'bye':
                reply = bot.get_response(message)
                if message.strip() == reply or reply.strip()=='I am sorry, but I do not understand.':
                     print('Kindly Contact Vidya/Monali for human assistance!!!')
                else:
                     print('Chatbot:',reply)
            if message.strip().lower() =='bye':
                print('Chatbot:Bye')
                break
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
