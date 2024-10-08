import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain import hub
from agent.chains.course_info_vector_chain import RAGSystem, RAGConfig
#from agent.chains.NLP_and_DL_vector_chain import NLP_and_DL_vector_chain
#from agent.chains.You_tube_vector_chain import You_tube_vector_chain
from agent.tools.factorial_fibonacci import (
    get_factorial,
    get_matrix_fibonacci,
)
from langchain.tools import StructuredTool
from pydantic import BaseModel
from langchain.agents import Tool, initialize_agent, AgentType
from typing import List, Dict, Any, Union

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

CS224N_AGENT_MODEL = os.getenv("CS224N_AGENT_MODEL")
# LANGCHAIN_API_KEY =  os.getenv("LANGCHAIN_API_KEY")

CS224N_agent_prompt = hub.pull("hwchase17/openai-functions-agent")
print(f'CS224N_agent_prompt:\n {CS224N_agent_prompt}')
print()

# set the LANGCHAIN_API_KEY environment variable (create key in settings)
from langchain import hub
# prompt = hub.pull("hwchase17/openai-functions-agent")


config = RAGConfig(
    model=os.getenv('CS224N_AGENT_MODEL'),
    embed_model=os.getenv('EMBED_MODEL'),
    chroma_db_path=os.getenv('CHROMA_DB_PATH')
)

rag_system = RAGSystem(config)


class Fib_Fact_Tool_Input(BaseModel):
    inp1: List[int]    
    #inp2: Dict

class Course_Info(BaseModel):
    inp1: List[str]

tools = [    
    StructuredTool(
        name="course_info",
        func=rag_system.course_info_vector_chain().invoke,
        # description="""Useful when you need to answer questions
        # about CS224N course 'Natural Language Processing with Deep Learning' 
        # itself for example Instructors, Course Manager, 
        # Teaching Assistants, Logistics, Previous offerings, Schedule, 
        # Reference Texts, Coursework, Course Materials etc.
        # Use the entire prompt as input to the tool.
        # For instance, if the prompt is:
        # "Is Chris Manning Instructor of CS224N Stanford course?", 
        # the input should be:
        # "Is Chris Manning Instructor of CS224N Stanford course?"
        # If you don't know answer - you answer should be 'I don't know.'
        # """,
        description='''Useful for answering questions about Transformers, 
        Natural Language Processing, attention and so on. 
        ''',
        args_schema=Course_Info,
    ),

    # Tool(
    #     name="NLP and DL materials",
    #     func=NLP_and_DL_vector_chain.invoke,
    #     description="""Useful for answering questions about any type of questions about 
    #     Natural Language Processing(NLP), Deep Learning(DL), Large Language models(LLMs), 
    #     Mashine Learning(ML). 
    #     For example questions about bag of words, embedings, word2vec, RNN, LSTM, Transformers, 
    #     attention, self-attention and any others questions about and around NLP, DL, LLMs, ML. 
    #     Use the entire prompt as input to the tool.
    #     For instance, if the prompt is:
    #     'What is Transformer?"
    #     the input should be:
    #     "Is Chris Manning Instructor of CS224N Stanford course?"
    #     'What is Transformer?"
    #     """,
    # ),
    # Tool(
    #     name="You tube lectures",
    #     func=You_tube_vector_chain,
    #     description="""Use when asked about YouTube lectures... 
    #     ......
    #     """,
    # ),
    StructuredTool(
        #1. Input only the number for which the factorial needs to be calculated. 
        # Do not include any additional words or phrases like "factorial of."
        name="factorial",
        func=get_factorial,
        description="""
        Purpose: Use this tool to calculate the exact factorial value of a given integer.              
        The tool will return a single number, which is the factorial of the input integer.
        """,
        args_schema=Fib_Fact_Tool_Input,
    ),
    StructuredTool(
        name="fibonachi",
        func=get_matrix_fibonacci,
        description="""
        Use when you need to find out exect value of fibonacci of the integer number.
        Do not pass the words "fibonacci of" as input, only the exectly integer number 
        of the factorial which value neeed to evalute. 
        This tool returns a one number which is fibonacci of number N.
        """,
        args_schema=Fib_Fact_Tool_Input,
    ),
]

chat_model = ChatOpenAI(
    model = CS224N_AGENT_MODEL,
    temperature=0,
)

#CS224N_agent_prompt = 
'''
input_variables=['agent_scratchpad', 'input'] optional_variables=['chat_history'] 

input_types={'chat_history': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]], 'agent_scratchpad': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]]} 

partial_variables={'chat_history': []} 

metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': 'openai-functions-agent', 'lc_hub_commit_hash': 'a1655024b06afbd95d17449f21316291e0726f13dcfaf990cc0d18087ad689a5'} 

messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], 
                                      template='You are useful agent. You aim is assist(Q&A) about CS224N Stanford course')), 
          MessagesPlaceholder(variable_name='chat_history', optional=True), 
          HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')), 
          MessagesPlaceholder(variable_name='agent_scratchpad')]
'''

CS224N_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt= CS224N_agent_prompt,
    tools=tools,
)

CS224N_rag_agent_executor = AgentExecutor(
    agent=CS224N_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)


#CS224N_agent_prompt = 
'''
input_variables=['agent_scratchpad', 'input'] optional_variables=['chat_history'] 

input_types={'chat_history': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]], 'agent_scratchpad': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]]} 

partial_variables={'chat_history': []} 

metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': 'openai-functions-agent', 'lc_hub_commit_hash': 'a1655024b06afbd95d17449f21316291e0726f13dcfaf990cc0d18087ad689a5'} 

messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], 
                                      template='You are useful agent. You aim is assist(Q&A) about CS224N Stanford course')), 
          MessagesPlaceholder(variable_name='chat_history', optional=True), 
          HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')), 
          MessagesPlaceholder(variable_name='agent_scratchpad')]
'''

