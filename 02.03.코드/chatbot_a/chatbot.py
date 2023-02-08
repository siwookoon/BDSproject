# import the libraries
import openai
import streamlit as st
from streamlit_chat import message
import requests

openai.api_key = st.secrets["api_secret"]
# Creating a function which will generate the calls from the api

def generate_response(prompt):
    if '부동산' in user_input:
        matching_dict = {'광진구' : '11215', '서초구' : '11650', '마포구' : '11440', '중랑구' : '11260', '구로구' : '11530'}
        result = ""
        for i in matching_dict.keys():
            if i in user_input:
                result = matching_dict[i]
        service_key = '4d42486779706d3034365957634870'
        #url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/{1+((j-1)*1000)}/{j*1000}'
        url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/1/5/2023/' + result
        print(url)
        req = requests.get(url)
        content = req.json()
        print(content)
        con = content['tbLnOpendataRentV']['row']
        a = ""
        for m in con:
            gu = str(m["SGG_NM"])
            dong = str(m["BJDONG_NM"])
            day = str(m["CNTRCT_DE"])
            gtn = str(m["RENT_GBN"])
            price = str(m["RENT_GTN"])
            a += (day +" : "+ gu + " " + dong +" "+ gtn +" "+ price +"만원")
            message = a
        return message
    else:
        completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
        message = completions.choices[0].text
        return message

st.title("chatBot : Streamlit + openAI")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You : ","Hello, how are you?", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    #store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1,- 1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
