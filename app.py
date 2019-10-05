from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os

app = Flask(__name__)
 
# Create a new chat bot named Charlie
# Create a new instance of a ChatBot

chatbot = ChatBot(
    'IsaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento, pero no entiendo',
            'maximum_similarity_threshold': 0.90
        }
    ],
    read_only=True,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ]
)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    #"chatterbot.corpus.spanish.greetings",
    "chatterbot.corpus.spanish.conversations",
    './static/conceptos.yml'
)

@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))
 
 
if __name__ == "__main__":
    app.run()