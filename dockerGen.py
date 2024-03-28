import os
import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = config.openai_key

def create_dockerfile(filename, flask_code, requirements):
    chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    messages = [
        SystemMessage(content="You're a helpful Docker assistant"),
        HumanMessage(content=f"Write me a Docker file for this code file main.py: {flask_code} With these requirements: {requirements}"),
    ]

    chat.invoke(messages)
    output = ""
    for chunk in chat.stream(messages):
        output = output + chunk.content

    start_index = output.find("```Dockerfile") + len("```Dockerfile")
    end_index = output.find("```", start_index)

    code_block = output[start_index:end_index]

    with open(filename, 'w') as file:
        file.write(code_block)

# filename = "./flask_test/Dockerfile"
# create_py_file(filename)
