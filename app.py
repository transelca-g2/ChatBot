from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os, json, yaml, sys
import mysql.connector

app = Flask(__name__)

connection = mysql.connector.connect(host='108.167.149.240', database='appcesco_chatbot', user='appcesco_chatbot', password='chatbot')

sql_select_Query = "SELECT p.pregunta, r.respuesta FROM preguntas p INNER JOIN respuestas r ON r.id_pregunta = p.id"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
rv = cursor.fetchall()

# Creación de file desde database
if os.path.isfile("./static/conceptosfile.yml"):
    os.remove("./static/conceptosfile.yml")

f = open("./static/conceptosfile.yml", "a")
data = dict([('categories', ['- Conceptos', '- Teoría']), ('conversations', dict(rv))])
f.write(yaml.dump(data, default_flow_style=False)) 
f.close()

# Create a new chat bot named Charlie
# Create a new instance of a ChatBot

chatbot = ChatBot(
    'dyna',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    #database_uri="mysql://chatbot:chatbot@localhost/chatbot",
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
# chatbot.storage.drop()

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    "chatterbot.corpus.spanish.greetings",
    "chatterbot.corpus.spanish.conversations",
    './static/conceptosfile.yml'
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
