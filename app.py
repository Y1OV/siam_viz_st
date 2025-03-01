import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import pandas as pd

st.set_page_config(page_title="Ikanam Service", layout="wide", page_icon="🏆")

def load_csv_data(csv_path):
    """Загружает CSV-файл с разметкой"""
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error("CSV-файл с разметкой не найден.")
        return None

def load_and_plot_data(directory, csv_path):
    """Загружает данные из 9 случайных файлов в директории, строит графики и отображает информацию из CSV"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if len(files) < 9:
        st.error("В директории должно быть минимум 9 файлов с данными.")
        return
    
    selected_files = random.sample(files, 9)
    csv_data = load_csv_data(csv_path)
    
    cols = st.columns(3)  
    
    for i, file in enumerate(selected_files):
        file_path = os.path.join(directory, file)
        try:
            data = np.loadtxt(file_path)
            time = data[:, 0] 
            pressure = data[:, 1] 
            derivative = data[:, 2]  
            
            with cols[i % 3]: 
                st.markdown(f"### {file}")
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.loglog(time, pressure, 'o', label='Давление')
                ax.loglog(time, derivative, 's', label='Производная давления')
                ax.set_xlabel("Время (часы)")
                ax.set_ylabel("Давление и производная (атм)")
                ax.legend()
                ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                
                st.pyplot(fig)
                
                if csv_data is not None:
                    row = csv_data[csv_data['file_name'] == file]
                    if not row.empty:
                        st.dataframe(row)
                    else:
                        st.warning("Файл отсутствует в CSV.")
        except Exception as e:
            st.error(f"Ошибка при обработке файла {file}: {e}")

st.title("Анализ данных давления")

directory = 'data'
csv_path = 'markup_train.csv'

if st.button("Загрузить и построить 9 рандомных графикоф"):
    if os.path.isdir(directory) and os.path.exists(csv_path):
        load_and_plot_data(directory, csv_path)
    else:
        st.error("Указанная директория или CSV-файл не существуют.")




