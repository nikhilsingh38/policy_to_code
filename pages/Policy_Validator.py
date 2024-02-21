import streamlit as st
import langchain_helper
import matplotlib.pyplot as plt
from collections import Counter
from ast import literal_eval
from pathlib import Path
import base64



st.set_page_config(page_title="Policy Validator", page_icon="📈",layout="wide")

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



triple_quote = ''' 
The Policy Validator automates the comparison of Rego code against user-provided policy documents to ensure compliance and correct enforcement. It streamlines policy validation, enhancing security and governance by identifying discrepancies and non-adherence efficiently.'''

st.title("Policy and Code Compliance Checker")
# st.sidebar.header("Policy Validator",help=triple_quote)

def draw_pie_chart(result):
    response = result["count"]
    lines = response.strip().split('\n')[2:]  # Exclude header rows

    compliance_status = [line.split('|')[2].strip() for line in lines]
    
    data={
        "Adherence": compliance_status
    }
    counts = Counter(data["Adherence"])
    # Calculate the percentage for each adherence type
    total = sum(counts.values())
    sizes = [count / total * 100 for count in counts.values()]

    colors = {"Yes": "#3EC300", "No": "#DD614A"}

    default_color = "#CCCCCC"  # Grey color for unspecified keys

    # Create the pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=counts.keys(), autopct='%1.1f%%', startangle=90,
            colors=[colors.get(key, default_color) for key in counts.keys()])
    ax1.axis('equal')# Equal aspect ratio ensures that pie is drawn as a circle.

    # Set the background color
    fig1.patch.set_facecolor('#0e1117')  # Sets the outer background color
    ax1.set_facecolor('#0e1117')  # Sets the inner plot background color

    # Change the text color to white
    for text in ax1.texts:
        text.set_color('white')

    st.pyplot(fig1)
    
    with open('./style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    # column_counter = 0

    # print(compliance_status)
    yes_count = compliance_status.count('Yes')
    no_count = compliance_status.count('No')

    col1.metric("Yes", yes_count)
    col2.metric("No", no_count)
        
        
   
    

with st.form(key='my_form'):
    uploaded_policy = st.file_uploader("Upload a Policy file", type=["txt", "pdf"])
    uploaded_code = st.file_uploader("Upload a Code file", type=["py", "rego", "txt"])
    submit_button = st.form_submit_button(label='Submit')

if uploaded_policy and uploaded_code:
    policy_text = langchain_helper.extract_text_from_file(uploaded_policy)
    code_text = uploaded_code.read()
    compliance_result = langchain_helper.check_compliance_with_gpt35(policy_text, code_text)
    
    ncol1, ncol2 = st.columns(2)
    
    with ncol1:
        st.write(compliance_result["issue"])
        st.text("")

    with ncol2:
        draw_pie_chart(compliance_result)
    
    
    
    # st.write(compliance_result["count"])
else:
    st.info("Please upload both a Policy file and a Code file.")