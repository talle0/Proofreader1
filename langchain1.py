import streamlit as st
import deepl
#API 키 저장을 위한 os 라이브러리 호출
import os
#OPENAI API 키 저장
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
DEEPL_API_KEY = st.secrets["DEEPL_API_KEY"]

# LLM 모델 설정
from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
aaa=OpenAI(model_name="gpt-3.5-turbo-instruct")
google = ChatGoogleGenerativeAI(model="gemini-pro")
claude = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
deeplt = deepl.Translator(DEEPL_API_KEY)

st.title("Your Proofreader")

def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "한국어" if k_count>e_count else "영어"
#print (isEnglishOrKorean(input))

def proofreading(input):
    # 영어 번역
    if isEnglishOrKorean(input) == "한국어":
        req1="I want you to act as a Korean-English translator. \
            Please translate following sentence to English: "+ input
        answer1=aaa.invoke(req1)
        st.write("영어 번역\n\n", answer1)
    else:
        answer1 = input
        st.write("영어 번역\n\n", answer1)

    # 학술 교정 (기본)
    st.markdown("---")
    academic1="I want you to act as an academic English proofreader. \
        Please proofread following sentences. \
        Please give me only edited sentences without any explanations: "+ answer1
    aca_basic=aaa.invoke(academic1)
    st.write("학술 교정 (기본) \n", aca_basic)

    # 학술 교정 (보다 학술적, ChatGPT)
    st.markdown("---")
    academic_high="I want you to act as an academic English proofreader. \
        Please change following sentences to more proper sentences for academic journals. \
        Please give me only edited sentences without any explanations: "+answer1
    aca_high=aaa.invoke(academic_high)
    st.write("학술 교정 (보다 학술적) \n", aca_high)

    # 학술 교정 (Google)
    st.markdown("---")
    academic_high="I want you to act as an academic English proofreader. \
        Please change following sentences to more proper sentences for academic journals. \
        Please give me only edited sentences without any explanations: "+answer1
    aca_goo=google.invoke(academic_high)
    st.write("학술 교정 (Google-Gemini)\n\n", aca_goo.content)

    # 학술 교정 (간단히, Google)
    st.markdown("---")
    academic_simple="I want you to act as an academic English proofreader. \
        Please change following sentences to more plain and simple sentences. \
        Please give me only edited sentences without any explanations: "+aca_high
    aca_simple=google.invoke(academic_simple)
    st.write("학술 교정 (보다 간단하고 이해하기 쉽게, Google-Gemini)\n\n", aca_simple.content)

    # 영어 번역 (Cluad3)
    st.markdown("---")
    if isEnglishOrKorean(input) == "한국어":
        req1="I want you to act as a Korean-English translator. \
            Please translate following sentence to English. \
            Please give me only edited sentences without any explanations: "+input
        answer1=claude.invoke(req1)
        st.write("Claud3\n\n", answer1.content)
    else:
        academic_claud="I want you to act as an academic English proofreader. \
        Please change following sentences to more proper sentences for academic journals. \
        Please give me only edited sentences without any explanations: "+input
        answer1 = claude.invoke(academic_claud)
        st.write("Claud3\n\n", answer1.content)

with st.form("Form 1"):
    input = st.text_area("한국어나 영어 문장을 넣어주세요", max_chars=5000, height=300,value="")
    s_state=st.form_submit_button("submit")
    if s_state:
        if (input == ""):
            st.warning ("원하는 교정 문장을 넣어주세요") 
        else:
            proofreading(input)




