import streamlit as st
from PIL import Image
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

from app.tools import AreasTool, GradosTool



st.set_page_config(page_title="Asistente USC")
st.title("Asistente USCBot 🤖")
stop = False

logo = Image.open("img/logo.jpg")

with st.sidebar:
    st.image(logo)
    if 'OPENAI_API_KEY' in st.secrets:
        st.success("OPENAI_API_KEY already provided!", icon='✅')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter your OPENAI_API_KEY: ', type='password')
        if not openai_api_key:
            st.warning('Please, enter your OPENAI_API_KEY', icon='⚠️')
            stop = True
        else:
            st.success('Preguntame tus dudas, te guiaré lo mejor que pueda!', icon='👉')

    st.markdown(""" Aqui podrás preguntar acerca de los grados disponibles y sus programas. Según tus intereses te ofreceré información que se adapte mejor a ti!
    """)

if stop:
    st.stop()

tools = [AreasTool(), GradosTool()]
messages = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=messages, return_messages=True)

fixed_prompt = '''Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant doesn't know anything about degrees in Universidad de Santiago de Compostela or other universities.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''

system_message = SystemMessage(content= fixed_prompt)


if len(messages.messages) == 0:
    messages.add_ai_message("Bienvenido a la USC, soy tu asistente personal y resolveré todas tus dudas encantado!")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=openai_api_key)
agent_kwargs = {
    "system_message": system_message,
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")]
}
open_ai_agent = initialize_agent(tools,
                                 llm,
                                 agent=AgentType.OPENAI_FUNCTIONS,
                                 agent_kwargs=agent_kwargs,
                                 verbose=True,
                                 memory=memory
                                 )

for msg in messages.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input(disabled= not openai_api_key):
    st.chat_message("human").write(prompt)
    with st.spinner("Thinking ..."):
        response = open_ai_agent.run(prompt)
        st.chat_message("ai").write(response)