import os.path
import matplotlib.pyplot as plt
from inference import get_results, frame_id_start
import streamlit as st
from datetime import datetime

st.title('Обнаружение негабаритов')

with st.sidebar:
    slider_size = st.slider('Размер негабарита (мм)', min_value=0, max_value=1000, step=1, value=1000)
    slider_class = st.slider('Класс негабарита', min_value=1, max_value=7, step=1)
    warning = st.empty()
    plot = st.empty()

frame = st.empty()

if os.getcwd() != 'streamlit_app':
    video_path = os.path.join(os.getcwd(), 'streamlit_app', 'video.mp4')
else:
    video_path = os.path.join(os.getcwd(), 'video.mp4')

for i in get_results(video_path):
    res = i['photo'].render()
    frame.image(res, width=400)
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
        fig, ax = plt.subplots()
        ax.plot(i['data']['oversize_plot_df'])
        plot.pyplot(fig)
