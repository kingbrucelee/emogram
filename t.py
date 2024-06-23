from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
import telebot
from telebot.types import Message
import re
from transformers import pipeline
from collections import defaultdict
from sentimentpl.models import SentimentPLModel

bot = telebot.TeleBot(BOT_TOKEN)

# Initialize sentiment analysis pipeline for English
sentiment_analyzer_en = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Initialize Polish sentiment analyzer
sentiment_analyzer_pl = SentimentPLModel(from_pretrained='latest')

def get_sentiment(text, lang='en'):
    if lang == 'pl':
        score = sentiment_analyzer_pl(text).item()
        label = "POSITIVE" if score > 0 else "NEGATIVE"
    else:
        result = sentiment_analyzer_en(text)[0]
        label, score = result['label'], result['score']
    return label, abs(score)

def extract_author_and_text(text):
    match = re.match(r'(.*?):\s*(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, text.strip()

@bot.message_handler(func=lambda message: True)
def analyze_sentiment(message: Message):
    if message.forward_from:
        messages = [(message.forward_from.first_name, message.text)]
    else:
        messages = [extract_author_and_text(msg.strip()) for msg in message.text.split('\n') if msg.strip()]
    
    results = defaultdict(list)
    
    for author, text in messages:
        # Detect language (simple method, you might want to use a more robust solution)
        lang = 'pl' if any(char in 'ąćęłńóśźż' for char in text.lower()) else 'en'
        
        sentiment, score = get_sentiment(text, lang)
        results[author or 'Unknown'].append((text, sentiment, score, lang))
    
    response = "Sentiment Analysis Results:\n\n"
    for author, analyses in results.items():
        response += f"Author: {author}\n"
        # Sort analyses by sentiment score (descending order)
        sorted_analyses = sorted(analyses, key=lambda x: x[2], reverse=True)
        for text, sentiment, score, lang in sorted_analyses:
            response += f"- Text: {text}\n"
            response += f"  Sentiment: {sentiment} (Score: {score:.2f}, Language: {lang})\n"
        response += "\n"
    
    bot.reply_to(message, response)

bot.polling()
