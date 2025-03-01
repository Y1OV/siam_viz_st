import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import pandas as pd
import asyncio
import concurrent.futures

st.set_page_config(page_title="Ikanam Service", layout="wide", page_icon="🏆")

async def load_csv_data(csv_path):
    """Загружает CSV-файл с разметкой асинхронно"""
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, pd.read_csv, csv_path)

async def load_file_data(file_path):
    """Асинхронно загружает данные из файла"""
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, np.loadtxt, file_path)

async def load_and_plot_data(directory, csv_path):
    """Загружает данные из 9 случайных файлов в директории, строит графики и отображает информацию из CSV"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if len(files) < 9:
        st.error("В директории должно быть минимум 9 файлов с данными.")
        return
    
    selected_files = random.sample(files, 9)
    
    try:
        csv_data = await load_csv_data(csv_path)
    except Exception as e:
        st.error(f"Ошибка загрузки CSV-файла: {e}")
        return
    
    cols = st.columns(3)
    
    tasks = [load_file_data(os.path.join(directory, file)) for file in selected_files]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, (file, result) in enumerate(zip(selected_files, results)):
        if isinstance(result, Exception):
            st.error(f"Ошибка при обработке файла {file}: {result}")
            continue
        
        data = result
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
            
            row = csv_data[csv_data['file_name'] == file]
            if not row.empty:
                st.dataframe(row)
            else:
                st.warning("Файл отсутствует в CSV.")

st.title("Анализ данных давления")

directory = 'data'
csv_path = 'markup_train.csv'

if st.button("Загрузить и построить 9 рандомных графиков"):
    if os.path.isdir(directory) and os.path.exists(csv_path):
        asyncio.run(load_and_plot_data(directory, csv_path))
    else:
        st.error("Указанная директория или CSV-файл не существуют.")




