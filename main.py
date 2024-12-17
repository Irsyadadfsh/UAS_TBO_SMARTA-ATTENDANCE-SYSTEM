import os.path
import datetime
import pickle

import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import face_recognition

import util


class LoginPage:
    def __init__(self):
        self.jendela_login = tk.Tk()
        self.jendela_login.geometry("400x300+500+200")
        self.jendela_login.title("Login")

        # Label dan Entry Username
        self.label_username = tk.Label(self.jendela_login, text="Username:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.jendela_login)
        self.entry_username.pack(pady=5)

        # Label dan Entry Password
        self.label_password = tk.Label(self.jendela_login, text="Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.jendela_login, show="*")
        self.entry_password.pack(pady=5)

        # Checkbox untuk menampilkan password
        self.show_password_var = tk.BooleanVar()
        self.checkbox_show_password = tk.Checkbutton(
            self.jendela_login,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility
        )
        self.checkbox_show_password.pack(pady=5)

        # Tombol Login
        self.button_login = tk.Button(self.jendela_login, text="Login", command=self.login)
        self.button_login.pack(pady=20)

    def toggle_password_visibility(self):
        # Ubah atribut 'show' dari entry password
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "12345678":
            self.jendela_login.destroy()
            app = Aplikasi(admin=True)  # Admin masuk
            app.mulai()
        elif username == "user" and password == "user123":
            self.jendela_login.destroy()
            app = Aplikasi(admin=False)  # User masuk
            app.mulai()
        else:
            messagebox.showerror("Error", "Username atau password salah!")

    def mulai(self):
        self.jendela_login.mainloop()


class Aplikasi:
    def __init__(self, admin):
        self.admin = admin
        self.jendela_utama = tk.Tk()
        self.jendela_utama.geometry("1200x520+350+100")

        # Tombol Login dan Logout
        self.tombol_login = util.get_button(self.jendela_utama, 'Login', 'green', self.login)
        self.tombol_login.place(x=750, y=10)

        self.tombol_logout = util.get_button(self.jendela_utama, 'Logout', 'red', self.logout)
        self.tombol_logout.place(x=750, y=110)

        # Tombol untuk Admin
        if self.admin:
            # Tombol Daftar Pengguna Baru
            self.tombol_registrasi = util.get_button(self.jendela_utama, 'Daftar Pengguna Baru', 'gray',
                                                     self.daftar_pengguna_baru, fg='black')
            self.tombol_registrasi.place(x=750, y=210)

            # Tombol Unduh File Log
            self.tombol_unduh_log = util.get_button(self.jendela_utama, 'Unduh Log', 'blue', self.unduh_log)
            self.tombol_unduh_log.place(x=750, y=310)

            # Tombol Kembali ke Halaman Login
            self.tombol_kembali_login_admin = util.get_button(self.jendela_utama, 'Kembali ke Login', 'orange',
                                                              self.kembali_ke_login)
            self.tombol_kembali_login_admin.place(x=750, y=410)

        else:
            # Tombol Kembali ke Halaman Login untuk User
            self.tombol_kembali_login_user = util.get_button(self.jendela_utama, 'Kembali ke Login', 'orange',
                                                             self.kembali_ke_login)
            self.tombol_kembali_login_user.place(x=750, y=210)

        # Label untuk Kamera
        self.label_webcam = util.get_img_label(self.jendela_utama)
        self.label_webcam.place(x=10, y=0, width=700, height=510)

        self.tambahkan_kamera(self.label_webcam)

        # Direktori Database Pengguna
        self.direktori_db = './db'
        if not os.path.exists(self.direktori_db):
            os.mkdir(self.direktori_db)

        # Lokasi File Log
        self.lokasi_log = './log.txt'

    def tambahkan_kamera(self, label):
        if 'kamera' not in self.__dict__:
            self.kamera = cv2.VideoCapture(0)

        self._label = label
        self.proses_kamera()

    def proses_kamera(self):
        ret, frame = self.kamera.read()
        frame = cv2.flip(frame, 1)
        self.gambar_terakhir = frame

        gambar_rgb = cv2.cvtColor(self.gambar_terakhir, cv2.COLOR_BGR2RGB)
        self.gambar_pil = Image.fromarray(gambar_rgb)
        gambar_tk = ImageTk.PhotoImage(image=self.gambar_pil)
        self._label.imgtk = gambar_tk
        self._label.configure(image=gambar_tk)

        self._label.after(20, self.proses_kamera)

    def login(self):
        nama = util.kenali(self.gambar_terakhir, self.direktori_db)

        if nama in ['pengguna_tidak_dikenal', 'tidak_ada_pengguna']:
            util.msg_box('Ups...', 'Pengguna tidak dikenal. Silakan daftar atau coba lagi.')
        else:
            util.msg_box('Selamat Datang!', f'Selamat datang, {nama}.')
            with open(self.lokasi_log, 'a') as f:
                f.write(f'{nama},{datetime.datetime.now()},masuk\n')

    def logout(self):
        nama = util.kenali(self.gambar_terakhir, self.direktori_db)

        if nama in ['pengguna_tidak_dikenal', 'tidak_ada_pengguna']:
            util.msg_box('Ups...', 'Pengguna tidak dikenal. Silakan daftar atau coba lagi.')
        else:
            util.msg_box('Sampai Jumpa!', f'Sampai jumpa, {nama}.')
            with open(self.lokasi_log, 'a') as f:
                f.write(f'{nama},{datetime.datetime.now()},keluar\n')

    def daftar_pengguna_baru(self):
        self.jendela_daftar = tk.Toplevel(self.jendela_utama)
        self.jendela_daftar.geometry("1200x520+370+120")

        self.tombol_terima = util.get_button(self.jendela_daftar, 'Terima', 'green', self.terima_pendaftaran)
        self.tombol_terima.place(x=750, y=300)

        self.tombol_coba_lagi = util.get_button(self.jendela_daftar, 'Coba Lagi', 'red', self.coba_lagi_pendaftaran)
        self.tombol_coba_lagi.place(x=750, y=400)

        self.label_gambar = util.get_img_label(self.jendela_daftar)
        self.label_gambar.place(x=10, y=0, width=700, height=500)

        self.tambahkan_gambar_ke_label(self.label_gambar)

        self.entri_nama = util.get_entry_text(self.jendela_daftar)
        self.entri_nama.place(x=750, y=150)

        self.label_text = util.get_text_label(self.jendela_daftar, 'Silakan masukkan nama pengguna:')
        self.label_text.place(x=750, y=70)

    def coba_lagi_pendaftaran(self):
        self.jendela_daftar.destroy()

    def tambahkan_gambar_ke_label(self, label):
        gambar_tk = ImageTk.PhotoImage(image=self.gambar_pil)
        label.imgtk = gambar_tk
        label.configure(image=gambar_tk)

        self.gambar_cadangan = self.gambar_terakhir.copy()

    def mulai(self):
        self.jendela_utama.mainloop()

    def terima_pendaftaran(self):
        nama = self.entri_nama.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.gambar_cadangan)[0]

        file = open(os.path.join(self.direktori_db, '{}.pickle'.format(nama)), 'wb')
        pickle.dump(embeddings, file)

        util.msg_box('Berhasil!', 'Pengguna berhasil didaftarkan!')

        self.jendela_daftar.destroy()

    def unduh_log(self):
        try:
            with open(self.lokasi_log, 'r') as file:
                data = file.read()
            util.msg_box('Log File', data)
        except FileNotFoundError:
            util.msg_box('Error', 'File log tidak ditemukan.')

    def kembali_ke_login(self):
        self.jendela_utama.destroy()
        login_page = LoginPage()
        login_page.mulai()

    def unduh_log(self):
        if os.path.exists(self.lokasi_log):
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")],
                                                     initialfile="log.txt")
            if file_path:
                with open(self.lokasi_log, 'r') as f:
                    data = f.read()
                with open(file_path, 'w') as f:
                    f.write(data)
                util.msg_box("Berhasil!", "File log berhasil diunduh!")
        else:
            util.msg_box("Error!", "File log tidak ditemukan!")


if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mulai()
