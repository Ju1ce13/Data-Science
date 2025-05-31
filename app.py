import streamlit as st
from analysis_and_model import analysis_and_model_page
from presentation import presentation_page


def main():
    """Главный интерфейс приложения с навигацией."""
    st.set_page_config(page_title="Predictive Maintenance App", layout="wide")

    st.sidebar.title("Навигация")
    pages = {
        "🧪 Анализ и модель": analysis_and_model_page,
        "📊 Презентация проекта": presentation_page
    }

    selected_page = st.sidebar.radio("Выберите раздел:", list(pages.keys()))
    pages[selected_page]()


if __name__ == "__main__":
    main()
