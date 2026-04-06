import streamlit as st
import PyPDF2
import docx
import re
import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LECTURER AUDIT SHIELD v4.2", layout="wide")

# Stopwords umum untuk penggunaan universal
STOPWORDS = {
    'dan', 'yang', 'adalah', 'untuk', 'dengan', 'dalam', 'dari', 'pada', 'saya', 'anda', 
    'ini', 'itu', 'atau', 'tugas', 'modul', 'mahasiswa', 'jawaban', 'soal',
    'jelaskan', 'berikan', 'contoh', 'masing', 'secara', 'tersebut', 'tentang', 
    'seperti', 'karena', 'melalui', 'nim', 'nama', 'prodi', 'fakultas', 'universitas'
}

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = " ".join([p.extract_text() or "" for p in reader.pages])
        elif ext == '.docx':
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
    except: return ""
    return text

def clean_text_pro(text):
    words = re.findall(r'[a-z]{3,}', text.lower())
    return [w for w in words if w not in STOPWORDS]

def get_ngrams(word_list, n=5):
    return [" ".join(word_list[i:i+n]) for i in range(len(word_list)-n+1)]

# --- UI INTERFACE ---
st.title("🛡️ SCANNER v4.2")
st.subheader("Similarity & Content Anomaly Notation & Evaluation Report")
st.markdown("Arismunandar, M.T.I. (c) 2026")
st.markdown("---")

matkul = st.sidebar.text_input("Nama Mata Kuliah:", value="Mata Kuliah Umum")
path_input = st.text_input("Masukkan Path Folder Tugas:", placeholder="D:\\tugas_mahasiswa")

if st.button("🔍 1. Scan & Siapkan Data"):
    clean_path = path_input.replace('"', '').replace("'", "").strip()
    if os.path.exists(clean_path):
        all_files = []
        for root, dirs, files in os.walk(clean_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx')):
                    f_p = os.path.join(root, file)
                    all_files.append({'path': f_p, 'size': os.path.getsize(f_p) / 1024})
        
        if all_files:
            st.session_state['ready_files'] = all_files
            st.success(f"✅ Terdeteksi {len(all_files)} file. Siap dianalisis.")
        else: st.error("❌ File tidak ditemukan.")
    else: st.error("❌ Path tidak valid.")

if 'ready_files' in st.session_state:
    if st.button("🚀 2. Jalankan Audit & Tampilkan Dashboard"):
        data_ngrams = {}
        file_info = {}
        files = st.session_state['ready_files']
        
        # Ekstraksi dan Analisis Text
        for item in files:
            f_path = item['path']
            display_name = f"{os.path.basename(os.path.dirname(f_path))} / {os.path.basename(f_path)}"
            cleaned = clean_text_pro(extract_text(f_path))
            data_ngrams[display_name] = set(get_ngrams(cleaned, n=5))
            file_info[display_name] = {
                'size': item['size'], 
                'is_empty': len(cleaned) < 10, # Threshold teks sangat minim
                'max_score': 0,
                'has_anomaly': False
            }

        # Kalkulasi Skor antar Pasangan
        hasil_lengkap = []
        for f1, f2 in combinations(data_ngrams.keys(), 2):
            set1, set2 = data_ngrams[f1], data_ngrams[f2]
            score = (len(set1.intersection(set2)) / len(set1.union(set2))) * 100 if set1 and set2 else 0
            
            # Update skor tertinggi tiap individu
            file_info[f1]['max_score'] = max(file_info[f1]['max_score'], score)
            file_info[f2]['max_score'] = max(file_info[f2]['max_score'], score)
            
            # Cek Anomali (Nada Case)
            if file_info[f1]['size'] > 300 and file_info[f1]['is_empty']: file_info[f1]['has_anomaly'] = True
            if file_info[f2]['size'] > 300 and file_info[f2]['is_empty']: file_info[f2]['has_anomaly'] = True

            # Tampilkan di tabel jika kemiripan signifikan (>20%)
            if score >= 20 or file_info[f1]['has_anomaly'] or file_info[f2]['has_anomaly']:
                hasil_lengkap.append({
                    "Mahasiswa A": f1, "Mahasiswa B": f2, "Skor (%)": round(score, 2),
                    "Investigasi": f"A: {'ANOMALI' if file_info[f1]['has_anomaly'] else 'Normal'} | B: {'ANOMALI' if file_info[f2]['has_anomaly'] else 'Normal'}"
                })

        # --- LOGIKA CATEGORY (v4.2) ---
        red, yellow, green = 0, 0, 0
        for mhs in file_info:
            info = file_info[mhs]
            if info['max_score'] > 85 or info['has_anomaly']:
                red += 1
            elif info['max_score'] >= 25: # Ambang batas Kuning diturunkan
                yellow += 1
            else:
                green += 1

        # --- TAMPILAN DASHBOARD ---
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Integrity Circles")
            fig, ax = plt.subplots(figsize=(6, 6))
            lbls = ['Red (High)', 'Yellow (Med)', 'Green (Low)']
            vals = [red, yellow, green]
            clrs = ['#ff4d4d', '#ffcc00', '#2eb82e']
            
            if sum(vals) > 0:
                ax.pie(vals, labels=lbls, colors=clrs, autopct='%1.1f%%', startangle=140, 
                       wedgeprops={'edgecolor': 'white', 'linewidth': 3})
                ax.add_artist(plt.Circle((0,0), 0.70, fc='white'))
                plt.title(f"Integritas: {matkul}")
                st.pyplot(fig)

        with col2:
            st.markdown("### 📋 Summary")
            st.write(f"Total Peserta: **{len(file_info)}**")
            st.error(f"🔴 Circle 1: {red} Mhs (Kritis)")
            st.warning(f"🟡 Circle 2: {yellow} Mhs (Waspada)")
            st.success(f"🟢 Circle 3: {green} Mhs (Aman)")
            
            if hasil_lengkap:
                csv_df = pd.DataFrame(hasil_lengkap).sort_values(by="Skor (%)", ascending=False)
                st.download_button(f"📥 Download CSV Report", csv_df.to_csv(index=False).encode('utf-8'), f"Audit_{matkul}.csv")

        if hasil_lengkap:
            st.markdown("---")
            st.markdown("### 🚩 Detail Temuan (Skor > 20%)")
            st.table(pd.DataFrame(hasil_lengkap)[["Mahasiswa A", "Mahasiswa B", "Skor (%)", "Investigasi"]])