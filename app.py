from flask import Flask, render_template, request
import requests
from translate import Translator 
from PyDictionary import PyDictionary
import os
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def get_synonyms(word):
    try:
        response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
        response.raise_for_status()
        synonyms = [item['word'] for item in response.json()]
        return synonyms
    except requests.RequestException as e:
        logging.error(f"Error fetching synonyms: {e}")
        return []


def get_antonyms(word):
    try:
        response = requests.get(f"https://api.datamuse.com/words?rel_ant={word}")
        response.raise_for_status()
        antonyms = [item['word'] for item in response.json()]
        return antonyms
    except requests.RequestException as e:
        logging.error(f"Error fetching antonyms: {e}")
        return []


def get_meaning(word):
    dictionary = PyDictionary()
    try:
        res = dictionary.meaning(word)
        return res
    except Exception as e:
        logging.error(f"Error fetching meaning: {e}")
        return None



def get_translation(word, target_language='ta'):
     translator = Translator(to_lang=target_language)
     try:
         translation = translator.translate(word)
         return translation
     except Exception as e:
         logging.error(f"Error fetching translation: {e}")
         return None


@app.route('/', methods=['GET', 'POST'])
def index():
    word = None
    antonyms = []
    synonyms = []
    meaning = None
    translation = None
    if request.method == 'POST':
        word = request.form['word']
        logging.info(f"Fetching data for word: {word}")
        antonyms = get_antonyms(word)
        synonyms = get_synonyms(word)
        meaning = get_meaning(word)
        translation = get_translation(word)

    return render_template('index.html', word=word, antonyms=antonyms, synonyms=synonyms, meaning=meaning,
                           translation=translation)


if __name__ == "__main__":
    app.run(debug=True)
