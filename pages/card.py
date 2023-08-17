import streamlit as st
import hydralit_components as hc

st.set_page_config(layout="wide")
st.markdown(
"""
<style>
.css-1aumxhk {
    padding: 0;
    border: none;
    box-shadow: none;
}
</style>
""",
unsafe_allow_html=True
)

#can apply customisation to almost all the properties of the card, including the progress bar
theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}

cc = st.columns(4)

with cc[0]:
 # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
 hc.info_card(title='Some heading GOOD', content='All good!', sentiment='good',bar_value=77)
 hc.info_card(title='Some heading GOOD2', content='All good!', sentiment='good',bar_value=77)
 hc.info_card(title='Some heading GOOD3', content='All good!', sentiment='good',bar_value=77)
 

with cc[1]:
 hc.info_card(title='Some BAD BAD', content='This is really bad',bar_value=12,theme_override=theme_bad)
 hc.info_card(title='Some BAD BAD2', content='This is really bad',bar_value=12,theme_override=theme_bad)
 hc.info_card(title='Some BAD BAD3', content='This is really bad',bar_value=12,theme_override=theme_bad)

with cc[2]:
 hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral',bar_value=55)
 hc.info_card(title='Some NEURALsdc2', content='Oh yeah, sure.', sentiment='neutral',bar_value=55)
 hc.info_card(title='Some NEURALsd', content='Oh yeah, sure.', sentiment='neutral',bar_value=55)

with cc[3]:
 #customise the the theming for a neutral content
 hc.info_card(title='Some NEURALd',content='Maybe...',key='sec',bar_value=5,theme_override=theme_neutral)
 hc.info_card(title='Some NEURAL2sc',content='Maybe...',key='sec2',bar_value=5,theme_override=theme_neutral)
 hc.info_card(title='Some NEURAL3sdc',content='Maybe...',key='sec3',bar_value=5,theme_override=theme_neutral)


# # import streamlit as st
# c1, c2, c3 = st.columns(3)
# c4, c5, c6 = st.columns([6,3,2]) #just to highlight these are different cols

# with st.container():
#     with c1:
#         hc.info_card(title='Some heading GOOD1', content='All good!', sentiment='good',bar_value=77)
#     with c2:
#         hc.info_card(title='Some heading GOOD2', content='All good!', sentiment='good',bar_value=77)
#     with c3:
#         hc.info_card(title='Some heading GOOD3', content='All good!', sentiment='good',bar_value=77)
#     # c1.write("c1")
#     # c2.write("c2")
#     # c3.write("c3")

# with st.container():
#     c4.write("c4")
#     c5.write("c5")
#     c6.write("c6")