from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from flask import Blueprint, render_template, request, redirect, url_for, flash


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


index_bp = Blueprint('index', __name__)


template_messages = ChatPromptTemplate.from_messages([
    ("system", "Translate the text into {language}"),
    ("human", "{text}"),
])

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)
parser = StrOutputParser()

chain = template_messages | model | parser


def translate_text(text, language):
    response = chain.invoke({"language": language, "text": text})
    
    return response
    

@index_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['target_language']

        if not text :
            flash('Please enter some text to translate', 'warning')
            return redirect(url_for('index.index'))
        
        translation = translate_text(text, target_language)

        return render_template('index.html', translation=translation)
    return render_template('index.html')





