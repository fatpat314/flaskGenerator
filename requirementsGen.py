import os
import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = config.openai_key

def create_requirements(filename, flask_code):
    chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    messages = [
        SystemMessage(content="You're a helpful programing assistant"),
        HumanMessage(content=f"Write me a requirements.txt file for this code to run in a docker container: {flask_code}. Use Flask version 3.0.2. Ensure the following dependencies are installed: importlib_metadata version 7.1.0 itsdangerous version 2.1.2 Jinja2 version 3.1.3 MarkupSafe version 2.1.5 Werkzeug version 3.0.1 zipp version 3.18.1"),
    ]

    chat.invoke(messages)

    output = ""
    for chunk in chat.stream(messages):
        output = output + chunk.content

    start_index = output.find("```") + len("```")
    end_index = output.find("```", start_index)

    code_block = output[start_index:end_index]
    # print(output)

    with open(filename, 'w') as file:
        file.write(code_block)