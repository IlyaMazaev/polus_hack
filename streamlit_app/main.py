import os.path
import matplotlib.pyplot as plt
from inference import get_results, frame_id_start
import streamlit as st
from datetime import datetime
import logging

logging.basicConfig(level=logging.WARNING)

st.title('Обнаружение негабаритов')
slider_size = st.slider('Размер негабарита (мм)', min_value=0, max_value=1000, step=1)
slider_class = st.slider('Класс негабарита', min_value=1, max_value=7, step=1)

video_column, graph_column = st.columns(2)
with video_column:
    frame = st.empty()
    warning = st.empty()
    with graph_column:
        plot = st.empty()

if os.getcwd() != 'streamlit_app':
    video_path = os.path.join(os.getcwd(), 'streamlit_app', 'video.mp4')
else:
    video_path = os.path.join(os.getcwd(), 'video.mp4')

for i in get_results(video_path):
    with video_column:
        res = i['photo'].render()
        frame.image(res, width=None)
        if i['data']['class']:
            warning.warning('ПУСТАЯ ЛЕНТА!')
        if slider_class in i['data']['class']:
            warning.warning(f'ОБНАРУЖЕН НЕГАБАРИТ КЛАССА {slider_class}!  ' + str(datetime.now().strftime("%H:%M:%S")),
                            icon="⚠️")
        for size in i['data']['sizes']:
            if size >= slider_size:
                warning.warning(
                    f'ОБНАРУЖЕН НЕГАБАРИТ РАЗМЕРОМ {int(size)} мм!  ' + str(datetime.now().strftime("%H:%M:%S")),
                    icon="⚠️")
    with graph_column:
        fig, ax = plt.subplots()
        ax.plot(i['data']['oversize_plot_df'])
        plot.pyplot(fig)
