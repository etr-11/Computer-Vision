## Parking Occupancy Detection

Проект для оценки занятости парковочных мест по видеопотоку с камеры.

### Структура проекта

- **`parking.mp4`** – исходное видео парковки.
- **`grafika.py`** – расчёт гомографии.
- **`detection.py`** – основная логика детекции машин и анализа занятости мест.
- **`occupancy_frame1.json`** – пример результата анализа первого кадра (номер места и вероятность занятости).

### Пример вида сверху

![Top view пример](image.png)

### Пример результата оценки занятости парковочных мест

![Parking result 1](demonstration/parking1.jpg)
![Parking result 2](demonstration/parking2.jpg)

### Детекция и анализ занятости на основе стороннего проекта

Фрагмент демонстрационного видео: `demonstration/rzd_video.mp4`

![result 1](demonstration/rzd1.jpg)
![result 2](demonstration/rzd2.jpg)

### Пример гомографии с OpenCV на Python

![photo 1](demonstration/f1.jpg)
![photo 2](demonstration/f2.jpg)
![result](demonstration/result.jpg)

