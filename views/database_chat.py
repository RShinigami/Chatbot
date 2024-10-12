from flask import Blueprint, request, jsonify, render_template
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import create_openai_tools_agent
from langchain.agents import create_openai_functions_agent
from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os

database_chat_bp = Blueprint('database_chat', __name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Database configuration
username = os.getenv('DB_USERNAME', 'root')
password = os.getenv('DB_PASSWORD', 'rayen123')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '3306')
database_name = os.getenv('DB_NAME', 'chatbot')

# Create the database URI
db_uri = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'

# Create the SQLAlchemy engine and session
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

# Create an SQLDatabase instance
db = SQLDatabase.from_uri(db_uri)

# Create toolkit and agent executor
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()

messages = [
    HumanMessagePromptTemplate.from_template("{input}"),
    AIMessage(content=SQL_FUNCTIONS_SUFFIX),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]

prompt = ChatPromptTemplate.from_messages(messages)
prompt = prompt.partial(**context)

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

@database_chat_bp.route('/database_chat', methods=['GET', 'POST'])
def database_chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
        response = agent_executor.invoke({"input": user_input})
        return jsonify({"response": response["output"]})
    return render_template('database_chat.html', username="User")

@database_chat_bp.route('/database_chat')
def database_chat_page():
    if 'user' in session:
        username = session['user'][1]
        return render_template('database_chat.html', username=username)
    return redirect(url_for('login_bp.login'))
