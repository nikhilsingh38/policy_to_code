import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub


st.set_page_config(page_title="Multiple PDF's", page_icon=":books:",layout="wide")

st.markdown("""
<nav class="custom-navbar">
    <a href="/">
        <img src="data:image/png;base64,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" class="imgCon" alt="Logo" >    
    </a>
    <div class="navContainer">
        <button class="btn">About Product</button>
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
        </svg>
    </div>
</nav>
""", unsafe_allow_html=True)

with open('./ptc_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    # st.set_page_config(page_title="Chat with multiple PDFs",
    #                    page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    # st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

    user_question = st.text_input("Ask a question about your documents:")
    # if user_question:
    #     handle_userinput(user_question)

    
    # with st.sidebar:
    if st.button("Process"):
        with st.spinner("Processing"):
           
            # get pdf text
            raw_text = get_pdf_text(pdf_docs)

            # get the text chunks
            text_chunks = get_text_chunks(raw_text)

            # create vector store
            vectorstore = get_vectorstore(text_chunks)

            # create conversation chain
            chatgptOutput = get_conversation_chain(
                vectorstore)
            
            bot = st.chat_message("assistant")
            # human = st.chat_message("user")
            bot.write(chatgptOutput)
            # human.write("Hello Bot")

if __name__ == '__main__':
    main()
