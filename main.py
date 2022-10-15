from inference import get_results
import streamlit as st
from datetime import datetime

st.title('Обнаружение негабаритов')
frame = st.empty()
slider = st.slider('Параметр негабарита', min_value=1, max_value=7, step=1)

video_column, graph_column = st.columns(2)

for i in get_results('video.mp4'):
    res = i['photo'].render()
    frame.image(res)
    if slider in i['data']['class']:
        st.warning('ОБНАРУЖЕН НЕГАБАРИТ!  '+ str(datetime.now().strftime("%H:%M:%S")), icon="⚠️")
