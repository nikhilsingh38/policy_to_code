import streamlit as st
import langchain_helper
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from ast import literal_eval
from pathlib import Path
import base64



st.set_page_config(page_title="Policy Validator", page_icon="📈",layout="wide")

st.markdown("""
<nav class="custom-navbar">
    <a href="/">
        <img src="http://upscalenet.com/wp-content/uploads/2024/02/pwcLogo.png" class="imgCon" alt="Logo">
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
st.sidebar.header("Policy Validator",help=triple_quote)

def draw_pie_chart():
    response = compliance_result["count"]
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
    column_counter = 0

    print(compliance_status)
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
    compliance_result = langchain_helper.check_compliance_with_openai(policy_text, code_text)
    
    ncol1, ncol2 = st.columns(2)
    
    with ncol1:
        st.write(compliance_result["issue"])
        st.text("")

    with ncol2:
        draw_pie_chart()
    
    
    
    # st.write(compliance_result["count"])
else:
    st.info("Please upload both a Policy file and a Code file.")