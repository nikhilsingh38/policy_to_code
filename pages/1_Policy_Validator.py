import streamlit as st
import langchain_helper
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from ast import literal_eval
from pathlib import Path
import base64



st.set_page_config(page_title="Policy Validator", page_icon="📈")
st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("./pwcLogo.png")), unsafe_allow_html=True)
st.title("Policy and Code Compliance Checker")
# st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)
st.sidebar.header("Policy Validator")
st.sidebar.markdown(''' 
The Policy Validator automates the comparison of Rego code against user-provided policy documents to ensure compliance and correct enforcement. It streamlines policy validation, enhancing security and governance by identifying discrepancies and non-adherence efficiently.''')

def draw_pie_chart():
    count_of_adhere = compliance_result["count"]
    
    count_of_adhere_dict = literal_eval(count_of_adhere)
    data={
        "Adherence": count_of_adhere_dict
    }
    counts = Counter(data["Adherence"])
    # Calculate the percentage for each adherence type
    total = sum(counts.values())
    sizes = [count / total * 100 for count in counts.values()]

    colors = {"Adhere": "#3EC300", "Doesn't Adhere": "#DD614A"}

    default_color = "#CCCCCC"  # Grey color for unspecified keys

    # Create the pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=counts.keys(), autopct='%1.1f%%', startangle=90,
            colors=[colors.get(key, default_color) for key in counts.keys()])
    ax1.axis('equal')# Equal aspect ratio ensures that pie is drawn as a circle.

    # Set the background color
    fig1.patch.set_facecolor('black')  # Sets the outer background color
    ax1.set_facecolor('black')  # Sets the inner plot background color

    # Change the text color to white
    for text in ax1.texts:
        text.set_color('white')

    st.pyplot(fig1)
    
    with open('./style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    column_counter = 0

# Iterate over the dictionary items
    for key, value in count_of_adhere_dict.items():
    # Use col1 for even counter values, col2 for odd
        if column_counter % 2 == 0:
            col1.metric(key, str(value))
        else:
            col2.metric(key, str(value))
        
        # Increment the counter
        column_counter += 1
   
    

with st.form(key='my_form'):
    uploaded_policy = st.file_uploader("Upload a Policy file", type=["txt", "pdf"])
    uploaded_code = st.file_uploader("Upload a Code file", type=["py", "rego", "txt"])
    submit_button = st.form_submit_button(label='Submit')

if uploaded_policy and uploaded_code:
    policy_text = langchain_helper.extract_text_from_file(uploaded_policy)
    code_text = uploaded_code.read()
    compliance_result = langchain_helper.check_compliance_with_openai(policy_text, code_text)
    
    st.write(compliance_result["issue"])
    draw_pie_chart()
    
    
    
    # st.write(compliance_result["count"])
else:
    st.info("Please upload both a Policy file and a Code file.")