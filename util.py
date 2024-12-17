import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(jendela, teks, warna, perintah, fg='white'):
    tombol = tk.Button(
        jendela,
        text=teks,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=warna,
        command=perintah,
        height=2,
        width=20,
        font=('Helvetica bold', 20)
    )

    return tombol


def get_img_label(jendela):
    label = tk.Label(jendela)
    label.grid(row=0, column=0)
    return label


def get_text_label(jendela, teks):
    label = tk.Label(jendela, text=teks)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(jendela):
    teks_masuk = tk.Text(jendela, height=2, width=15, font=("Arial", 32))
    return teks_masuk


def msg_box(judul, deskripsi):
    messagebox.showinfo(judul, deskripsi)


def kenali(gambar, path_db):
    embeddings_tidak_dikenal = face_recognition.face_encodings(gambar)
    if len(embeddings_tidak_dikenal) == 0:
        return 'tidak_ada_pengguna'
    else:
        embeddings_tidak_dikenal = embeddings_tidak_dikenal[0]

    daftar_db = sorted(os.listdir(path_db))

    cocok = False
    indeks = 0
    while not cocok and indeks < len(daftar_db):
        path_file = os.path.join(path_db, daftar_db[indeks])

        file = open(path_file, 'rb')
        embeddings = pickle.load(file)

        cocok = face_recognition.compare_faces([embeddings], embeddings_tidak_dikenal)[0]
        indeks += 1

    if cocok:
        return daftar_db[indeks - 1][:-7]
    else:
        return 'pengguna_tidak_dikenal'
