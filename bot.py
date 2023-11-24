import telebot
import pandas as pd
from pandasai import Agent, SmartDataframe, SmartDatalake

TOKEN = '6396102788:AAEbjN1Xl3LuSE_WDQD8EiCQZJJFPSBq538'

# Iniciando o BOT
bot = telebot.TeleBot(TOKEN)

# Lendo o arquivo CSV
df = pd.read_csv('copasdomundo2.csv', delimiter=';')

# Convertendo para o formato desejado de forma dinâmica
result = {header.lower().replace(' ', '_'): df[header].tolist() for header in df.columns}

# Criando uma instância do modelo de linguagem
from pandasai.llm import OpenAI
llm = OpenAI(api_token="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")

sdf = SmartDataframe(result, config={"llm": llm})

@bot.message_handler(func=lambda message: True)
def responder_pergunta(mensagem):
    try:
        # Obtendo a pergunta do usuário
        pergunta_usuario = mensagem.text

        # Enviando a pergunta para o modelo de linguagem
        resposta = sdf.chat(pergunta_usuario)

        # Enviando a resposta de volta ao usuário no Telegram
        bot.reply_to(mensagem, resposta)
    
    except Exception as e:
        # Em caso de erro, envie uma mensagem indicando o problema
        bot.reply_to(mensagem, f"Erro durante sdf.chat: {e}")


# Iniciando o bot
bot.polling()
