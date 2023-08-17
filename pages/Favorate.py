import streamlit as st
import numpy as np

tab1, tab2 = st.tabs(["📈 Lists", "🗃 Map"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)



# import streamlit as st

# # def local_css(file_name):
# #     with open(file_name) as f:
# #         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # local_css("style.css")

# with st.sidebar:
#     st.button("button sidebar 1")
#     st.button("button sidebar longer text")
#     st.button("button sidebar 2")
#     st.button("button sidebar 3")

# st.button("button page 1")
# st.button("button longer text page")
# st.button("button page 2")
# st.button("button page 3")