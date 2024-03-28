import os
import config

from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = config.openai_key

def create_flask_file(filename):
    tools = [PythonREPLTool()]

    instructions = """You are an agent designed to write python code.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Output your code that answers the users request. 
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)

    agent = create_openai_functions_agent(ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"), tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    answer = agent_executor.invoke({"input": "Write me a Flask version 3.0.2 app that returns the 10th number of the fibonacci sequence as a sentence of words that runs on host 0.0.0.0 and port 5000."})
    output = answer['output']

    start_index = output.find("```python") + len("```python")
    end_index = output.find("```", start_index)

    code_block = output[start_index:end_index]

    with open(filename, 'w') as file:
        file.write(code_block)
    
    return(code_block)

# filename = "./flask_test/test.py"
# create_flask_file(filename)
