import streamlit as st
import streamlit_folium

from sekop_log_parsing import *

st.title('Навигационный трек из лог файла')

log_file = st.file_uploader(
    'Загрузить лог файл',
    type=['csv', 'csv gz', 'csv tar gz']
)

if not log_file is None:

    try:
        # Получение массива данных  NMEA из лога
        nmea_track = extract_nmea_from_log(log_file)

        # Преобразование  времени в datetime
        track_time = track_time_to_datetime(nmea_track[:, 0])

        # Пересчитываем координаты в десятичные градусы
        track = nmea_coordinates_to_degrees(nmea_track)[:, 1:3]

        # Приведение к виду для загрузки в leaflet/foliant:
        track2list = track.tolist()

        # Параметры баундингбокса
        bottom_right = [
            track.max(axis=0)[0],
            track.min(axis=0)[1]
        ]

        top_left = [
            track.min(axis=0)[0],
            track.max(axis=0)[1]
        ]

        # Центр баундингбокса
        center_dot = (np.array(bottom_right) + np.array(top_left)) / 2
        center_dot = center_dot.tolist()

        # Центрирование карты в центре баундингбокса
        my_map = folium.Map(location=center_dot)

        # Отрисовка трека точками
        draw_dot_track_to_map(my_map, track_time, track2list)

        # Трек линиями
        # draw_polyline_trip_track(my_map, track2list)

        # Автомасштаб по границам баундингбокса
        my_map.fit_bounds(
            [bottom_right, top_left],
            padding=top_left  # Отступы по краям (не понятно в каких единицах)
        )

        st_data = streamlit_folium.st_folium(
            my_map, width=725
        )


    except (KeyError, IndexError) as e:
        st.error(
            """
            ** Ошибка чтения файла. Попробуйте другой файл **
            """
        )


if __name__ == '__main__':
    pass
