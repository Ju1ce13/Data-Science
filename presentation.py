import streamlit as st
from typing import List, Dict
import time
from streamlit_autorefresh import st_autorefresh


# Слайды презентации
slides: List[Dict[str, str]] = [
    {
        "title": "🧾 Введение",
        "content": """
**Цель:** предсказать отказ оборудования (Target = 1) или его отсутствие (Target = 0).  
**Датасет:** 10 000 записей, 14 признаков (температура, момент, износ и т.д.)
        """
    },
    {
        "title": "🔄 Этапы проекта",
        "content": """
1. Загрузка и предобработка данных  
2. Масштабирование признаков  
3. Обучение модели  
4. Оценка результатов  
5. Интерфейс для прогноза
        """
    },
    {
        "title": "🧹 Предобработка данных",
        "content": """
- Удалены: `UDI`, `Product ID`, типы отказов (`TWF`, `HDF` и др.)  
- `Type`: L → 0, M → 1, H → 2  
- Масштабирование: `StandardScaler`
        """
    },
    {
        "title": "🧠 Модель",
        "content": """
- Алгоритм: **Random Forest**  
- Разделение: 80% обучение / 20% тест  
- Метрики: Accuracy, ROC-AUC, Confusion Matrix
        """
    },
    {
        "title": "📈 Результаты",
        "content": """
- Accuracy: ~0.95  
- ROC-AUC: ~0.97  
- Матрица ошибок визуализирована
        """
    },
    {
        "title": "💬 Интерфейс прогноза",
        "content": """
Ввод пользователем:  
- Тип, температуры, скорость, момент, износ  

Вывод:  
- Класс (0 или 1)  
- Вероятность отказа
        """
    },
    {
        "title": "📌 Выводы и улучшения",
        "content": """
✅ Модель работает точно  
🛠 Возможности:
- Добавить XGBoost, SVM  
- Подбор гиперпараметров  
- Интеграция с UCI или API
        """
    }
]

def presentation_page():
    st.title("📊 Презентация проекта")

    # Состояние
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0
    if "autoplay" not in st.session_state:
        st.session_state.autoplay = False
    if "last_run" not in st.session_state:
        st.session_state.last_run = time.time()

    idx = st.session_state.slide_index
    total = len(slides)

    # Автопрокрутка (3 секунды)
    if st.session_state.autoplay:
        count = st_autorefresh(interval=3000, limit=None, key="autorefresh")

        if time.time() - st.session_state.last_run > 2.5:
            if idx < total - 1:
                st.session_state.slide_index += 1
            else:
                st.session_state.autoplay = False
            st.session_state.last_run = time.time()

    # Отображение текущего слайда
    st.markdown(f"### {slides[idx]['title']}")
    st.markdown(slides[idx]["content"], unsafe_allow_html=True)

    st.divider()

    # Панель управления
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    with col1:
        if st.button("⏮ В начало", use_container_width=True):
            st.session_state.slide_index = 0

    with col2:
        if st.button("⬅️ Назад", use_container_width=True):
            st.session_state.slide_index = max(0, idx - 1)

    with col4:
        if st.button("➡️ Далее", use_container_width=True):
            st.session_state.slide_index = min(total - 1, idx + 1)

    with col5:
        if st.button("⏭ В конец", use_container_width=True):
            st.session_state.slide_index = total - 1

    # Прогресс-бар
    with col3:
        st.progress((idx + 1) / total, text=f"Слайд {idx + 1} из {total}")

    # Переключатель автопрокрутки
    autoplay_label = "⏸ Остановить автопрокрутку" if st.session_state.autoplay else "▶️ Автопрокрутка"
    if st.toggle(autoplay_label, key="autoplay_toggle"):
        st.session_state.autoplay = not st.session_state.autoplay
