import streamlit as st

st.title('Select the Category of your policy:')

# Create buttons for each policy category
if st.button('RBAC'):
    st.write('You selected RBAC.')
if st.button('Network Standards'):
    st.write('You selected Network Standards.')
if st.button('API Authorization'):
    st.write('You selected API Authorization.')
if st.button('Role-base Access'):
    st.write('You selected Role-base Access.')

# Create a submit button
if st.button('Submit'):
    st.write('Your selection has been submitted.')
