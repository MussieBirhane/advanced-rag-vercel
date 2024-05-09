from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())                  # read local .env file
openai_api_key  = os.getenv('OPENAI_API_KEY')
token = os.getenv('TELEGRAM_BOT_TOKEN')

# SQL database
from langchain_community.utilities.sql_database import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///database\chinook.db")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools")

## define a function here to import in the main source code