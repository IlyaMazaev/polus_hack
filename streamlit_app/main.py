import os.path
import matplotlib.pyplot as plt
from inference import get_results
import streamlit as st
from datetime import datetime
import logging

logging.basicConfig(level=logging.WARNING)

st.title('Обнаружение негабаритов')
slider = st.slider('Параметр негабарита', min_value=1, max_value=7, step=1)

video_column, graph_column = st.columns(2)
with video_column:
    frame = st.empty()
    warning = st.empty()
    with graph_column:
       plot = st.empty()

for i in get_results(os.path.join(os.getcwd(), 'video.mp4')):
    with video_column:
        res = i['photo'].render()
        frame.image(res)
        if slider in i['data']['class']:
            warning.warning('ОБНАРУЖЕН НЕГАБАРИТ!  '+ str(datetime.now().strftime("%H:%M:%S")), icon="⚠️")
    with graph_column:
       fig, ax = plt.subplots()
       ax.plot(i['data']['oversize_plot_df'])
       plot.pyplot(fig)
