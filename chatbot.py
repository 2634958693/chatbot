import streamlit as st
from streamlit_chat import message
import SparkApi

appid = "65b363b0"
api_secret = "NjUzZjExZmQ3NTEyZWZkMDExNjNkMWYx"
api_key = "0c010fc6b52e23afb97140168ba3887f"

domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"

text = []

def getText(role, content):
    """
    构造包含角色和内容的对话信息，并添加到对话列表中

    参数：
    role (str): 对话角色，可以是 "user"（用户）或 "assistant"（助手）
    content (str): 对话内容

    返回值：
    text (list): 更新后的对话列表
    """
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    """
    计算对话列表中所有对话内容的字符长度之和

    参数：
    text (list): 对话列表

    返回值：
    length (int): 对话内容的字符长度之和
    """
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    """
    检查对话列表中的对话内容字符长度是否超过限制（8000个字符）
    如果超过限制，删除最早的对话内容，直到满足字符长度限制

    参数：
    text (list): 对话列表

    返回值：
    text (list): 更新后满足字符长度限制的对话列表
    """
    while getlength(text) > 8000:
        del text[0]
    return text


# 初始化对话历史和生成的响应列表
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if "entry" not in st.session_state:
    st.session_state["entry"] = False

st.set_page_config(
    page_title="AI-Chat App",
    page_icon=":robot:",
)

def on_input_change(user_input):
    if user_input:
        # 构造用户输入的对话信息
        question = checklen(getText("user", user_input))

        # 调用 SparkApi 中的函数进行问题回答
        SparkApi.answer = ""
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        output = getText("assistant", SparkApi.answer)

        # 将用户输入和生成的响应添加到对话历史和生成的响应列表中
        st.session_state['past'].append(user_input)
        if len(str(output[-1]['content']))>0:
            st.session_state['generated'].append(str(output[-1]['content']))
        else:
            st.session_state['generated'].append("当前请求发生错误！")

st.markdown('''<style>
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="block-container"] {
        padding-bottom: 40px;
        padding-top: 40px;
    }
    .main {
        background-color: #f5f5f5d4;
    }
    [data-testid="stTextInput"] input {
        border: none !important;
        -webkit-box-shadow: inset 5px 5px 5px rgba(0, 0, 0, .2), inset -5px -5px 5px #fff;
        box-shadow: inset 5px 5px 5px rgba(0, 0, 0, .2), inset -5px -5px 5px #fff;
        //border-radius: 20px !important;
        //padding: 2em
    }
    [data-testid="stTextInput"],
    [data-testid="stExpander"] {
        border: none !important;
        -webkit-box-shadow: 5px 5px 5px rgba(0, 0, 0, .2), -5px -5px 5px #fff;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, .2), -5px -5px 5px #fff;
        border-radius: 0.5rem !important;
        //text-align: center;
        padding: 1em
    }
    </style>''', unsafe_allow_html=True)
    
s = '''
border: none !important;
        -webkit-box-shadow: 5px 5px 5px rgba(0, 0, 0, .2), -5px -5px 5px #fff;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, .2), -5px -5px 5px #fff;
        border-radius: 0.5rem;
        //text-align: center;
        padding: 1em;'''

if st.session_state["entry"] == False:
    st.markdown('''<div style="height:200px;"><div>''', unsafe_allow_html=True)
    col = st.columns(5)
    col[2].image("https://docs.dknowc.cn/20220424/1531/41fbc4a5-2ebc-488f-8427-e205c7d19960/%E5%BD%A9%E6%99%BA%E6%9C%BA%E5%99%A8%E4%BA%BA.png", use_column_width=True)
    col = st.columns(3)
    entry = col[1].button("进入AI智能教学服务平台", use_container_width=True, key="button1")
    
    if entry:
        st.session_state["entry"] = True
        st.rerun()

if st.session_state["entry"]:
    st.markdown(f'<h1 id ="title" style="text-align: center; font-size: 24px; color: white; background: rgba(251,196,36); border-radius: .5rem; margin-bottom: 25px;{s}">AI智能教学服务平台</h1>', unsafe_allow_html=True)

    user_input = st.text_input("问题输入：", key="user_input")
    on_input_change(user_input)

    if st.session_state['generated']:
        with st.expander(f"共{len(st.session_state.past)+len(st.session_state.generated)}条聊天记录", True):
            for i in range(0, len(st.session_state['generated']), 1):
                message(st.session_state['past'][::-1][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][::-1][i], key=str(i))
    else:
        with st.expander(f"共{len(st.session_state.past)+len(st.session_state.generated)}条聊天记录", True):
            st.info("欢迎来到AI智能问答系统,当前无任何聊天记录!")
