from dotenv import load_dotenv
load_dotenv()

from langchain_community.agent_toolkits import GmailToolkit
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

toolkit = GmailToolkit()

memory = ChatMessageHistory()


llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''You are a helpful assistant for the support team of the company Finlogik. You may not need to use tools for every query - the user may just want to chat!
            when the user asks about his emails always check if the emails is about a problem if yes categprize the email 
            there are 4 categories:
            cat 1 : Access Issue : problems related to not able to access your account(like linkedin or faceboook account)
            cat 2 : Network Issue : problems related to connections failures
            cat 3 : Hardware Failure : problems related to the hardwares (like booting or some equipement wont work)
            cat 4 : Software Failure : problem related to softwares (like not being able to download something)
            if the emails is about one of these problems then answer in this format "username : sender's username  \n category : name of the the category of the email" \n the problem : prolem within the email 
            else if there is a normal email answer in this format "username : sender's username , \n content : the emails content"
            ''',
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=False,
)

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
)

def process_chat(user_input):
    response = conversational_agent_executor.invoke(
        {"input": user_input},
        {"configurable": {"session_id": "unused"}}
    )
    return response["output"]
