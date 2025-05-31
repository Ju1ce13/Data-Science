import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Предобработка данных: удаление лишнего, кодирование и масштабирование."""
    df = df.drop(columns=['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'])
    df['Type'] = df['Type'].map({'L': 0, 'M': 1, 'H': 2})

    numeric_features = ['Air temperature [K]', 'Process temperature [K]',
                        'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    return df, scaler


def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Обучение модели Random Forest."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


def display_metrics(y_true, y_pred, y_proba):
    """Отображение метрик модели."""
    st.subheader("Результаты оценки модели")
    st.write(f"**Accuracy:** {accuracy_score(y_true, y_pred):.2f}")
    st.write(f"**ROC-AUC:** {roc_auc_score(y_true, y_proba):.2f}")

    fig, ax = plt.subplots()
    sns.heatmap(confusion_matrix(y_true, y_pred), annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title("Матрица ошибок")
    st.pyplot(fig)


def predict_failure(model, scaler, numerical_cols: list[str]):
    """Форма для ввода данных и предсказание отказа оборудования."""
    st.subheader("Ввод данных для прогноза")

    with st.form("input_form"):
        input_data = {
            'Type': st.selectbox("Тип оборудования", options=['L', 'M', 'H']),
            'Air temperature [K]': st.number_input("Температура воздуха [K]", value=300.0),
            'Process temperature [K]': st.number_input("Температура процесса [K]", value=310.0),
            'Rotational speed [rpm]': st.number_input("Скорость вращения [rpm]", value=1500.0),
            'Torque [Nm]': st.number_input("Крутящий момент [Nm]", value=40.0),
            'Tool wear [min]': st.number_input("Износ инструмента [min]", value=100.0),
        }

        submitted = st.form_submit_button("Сделать прогноз")

    if submitted:
        input_df = pd.DataFrame([input_data])
        input_df['Type'] = input_df['Type'].map({'L': 0, 'M': 1, 'H': 2})
        input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        st.markdown("### Результат предсказания:")
        st.write("**Отказ оборудования**" if prediction == 1 else "**Оборудование работает нормально**")
        st.write(f"**Вероятность отказа:** {probability:.2f}")


def analysis_and_model_page():
    st.title("Анализ и модель")

    uploaded_file = st.file_uploader("Загрузите CSV-файл", type="csv")
    if not uploaded_file:
        return

    df = pd.read_csv(uploaded_file)
    df, scaler = preprocess_data(df)

    target_col = 'Machine failure'
    feature_cols = df.drop(columns=[target_col]).columns.tolist()
    numerical_cols = ['Air temperature [K]', 'Process temperature [K]',
                      'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

    X = df[feature_cols]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    display_metrics(y_test, y_pred, y_proba)
    predict_failure(model, scaler, numerical_cols)
