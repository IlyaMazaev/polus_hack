import os.path
import matplotlib.pyplot as plt
from inference import get_results, frame_id_start
import streamlit as st
from datetime import datetime
import logging

logging.basicConfig(filename='logs.log', level=logging.WARNING)

# from alchemy_class import Oversize
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# engine = create_engine("sqlite:///:memory:")
# Session = sessionmaker(bind=engine)
# Session.configure(bind=engine)
# session = Session()

st.title('Обнаружение негабаритов')

frame = st.empty()

with st.sidebar:
    slider_size = st.slider('Размер негабарита (мм)', min_value=0, max_value=1000, step=1, value=1000)
    slider_class = st.slider('Класс негабарита', min_value=1, max_value=7, step=1)
    warning = st.empty()
    plot = st.empty()

if os.getcwd() != '/streamlit_app':
    video_path = os.path.join(os.getcwd(), 'streamlit_app', 'video.mp4')
else:
    video_path = os.path.join(os.getcwd(), 'video.mp4')

for i in get_results(video_path):
    res = i['photo'].render()
    frame.image(res, width=800)
    if len(i['data']['class']) == 0:
        warning.warning('ПУСТАЯ ЛЕНТА!')
    if slider_class in i['data']['class']:
        warning.warning(f'ОБНАРУЖЕН НЕГАБАРИТ КЛАССА {slider_class}!  ' + str(datetime.now().strftime("%H:%M:%S")),
                        icon="⚠️")
        logging.warning(f'ОБНАРУЖЕН НЕГАБАРИТ КЛАССА {slider_class}!  ' + str(datetime.now().strftime("%H:%M:%S")))

        # session.add(Oversize(stone_class=slider_class, datetime=str(datetime.now().strftime("%H:%M:%S"))))
        # session.commit()
    for size in i['data']['sizes']:
        if size >= slider_size:
            warning.warning(
                f'ОБНАРУЖЕН НЕГАБАРИТ РАЗМЕРОМ {int(size)} мм!  ' + str(datetime.now().strftime("%H:%M:%S")),
                icon="⚠️")
            logging.warning(f'ОБНАРУЖЕН НЕГАБАРИТ РАЗМЕРОМ {int(size)} мм!  ' + str(datetime.now().strftime("%H:%M:%S")))
    fig, ax = plt.subplots()
    ax.plot(i['data']['oversize_plot_df'])
    plot.pyplot(fig)
