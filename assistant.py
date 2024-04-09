import streamlit as st
from PIL import Image
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

from app.tools import AreasTool, EstudiosTool, NotasTool, BecasTool, CalendarioTool, DeportesTool


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

page_img = """
<style>
[data-testid="stSidebar"] {
background-color: #f0f2f6
}
</style>
"""
st.markdown(page_img, unsafe_allow_html=True)

stop = False
logo = Image.open("img/logo_usc.png")
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
            st.success('Pregúntame tus dudas, te guiaré lo mejor que pueda!', icon='👉')



if stop:
    st.stop()

tools = [AreasTool(), EstudiosTool(), NotasTool(), BecasTool(), CalendarioTool(), DeportesTool()]
messages = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=messages, return_messages=True)

with st.sidebar:
    col_1, col_2, col_3 = st.columns((0.8,1,0.5))
    if col_2.button("Reset Chat"):
        messages.clear()
        memory.clear()


fixed_prompt = '''Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant doesn't know anything about information related to the Universidad de Santiago de Compostela or other universities.

Assistant doesn't know anything about the university calendar.

Assistant will use 'DeportesTool' tool to offer information about any sport activity.

Assistant will use 'NotasTool' tool only once to the answer a user question about notas of every degree of a certain area.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide summarized and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Assistant will answer concisely without further information.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''

system_message = SystemMessage(content= fixed_prompt)


if len(messages.messages) == 0:
    initial_message = "Bienvenido a la USC, soy tu asistente personal y resolveré todas tus dudas encantado!\n"\
                      "\n"\
                      "Aqui tienes un atajo a la información disponible:\n"\
                      "- Áreas de estudio con sus grados y másteres.\n"\
                      "- Notas de corte por grado.\n"\
                      "- Portal de becas.\n"\
                      "- Calendario del curso actual.\n"\
                      "- Instalaciones deportivas y actividades."
    messages.add_ai_message(initial_message)

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

def input_response(human_prompt):
    with st.spinner("Rebuscando en mis archivos..."):
        open_ai_agent.run(human_prompt)


load_css()


centered_title = """
<h1 style="text-align: center;">
    <img src="app/static/ai_icon.png" style="vertical-align: middle; width: 50px; height: 50px;"> Asistente USC
</h1>
"""

st.markdown(centered_title, unsafe_allow_html=True)

chat_placeholder = st.container()

if human_prompt := st.chat_input(placeholder= "Escribe tu pregunta",disabled= not openai_api_key):
    input_response(human_prompt)

with chat_placeholder:
    for msg in messages.messages:
        div = f"""
<div class="chat-row 
    {'' if msg.type == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="app/static/{
        'ai_icon.png' if msg.type == 'ai'
        else 'user_icon.png'}"
         width=32 height=32>
    <div class="chat-bubble
    {'ai-bubble' if msg.type == 'ai' else 'human-bubble'}">
        &#8203;{msg.content}
    </div>
</div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")
