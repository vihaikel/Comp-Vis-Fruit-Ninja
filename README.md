# Computer Vision - Fruit Ninja

Game Fruit Ninja sederhana berbasis computer vision. Pemain menggerakkan
ujung jari telunjuk di depan kamera untuk membuat gerakan tebasan dan
memotong buah yang muncul di layar.

## Fitur

- Pelacakan satu tangan menggunakan MediaPipe Hands.
- Posisi ujung jari telunjuk digunakan sebagai kursor/tebasan.
- Jejak gerakan jari divisualisasikan sebagai garis berwarna cyan.
- Buah muncul dari bagian bawah layar dengan lintasan dan warna acak.
- Buah yang terkena garis tebasan menambah skor (+10), buah yang terlewat
  mengurangi skor (-5).
- Level meningkat setiap 150 poin dan membuat lontaran buah lebih cepat serta
  lebih menyebar.
- Layar "LEVEL UP!" dengan animasi teks, konfeti, dan efek suara (dibuat
  langsung dengan kode, tanpa file audio) setiap naik level.
- Tampilan kamera digunakan sebagai latar belakang permainan.

## Persyaratan

- Windows dengan Python 3.11 (disarankan Python `3.11.16`).
- Webcam yang dapat diakses oleh OpenCV.
- Pencahayaan yang cukup agar tangan mudah dideteksi kamera.

## Instalasi

Buka Command Prompt atau PowerShell di folder proyek, lalu jalankan:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika menggunakan Command Prompt, perintah aktivasi yang sama dapat digunakan.
Untuk keluar dari virtual environment, jalankan:

```bat
deactivate
```

## Menjalankan Game

Pastikan webcam tidak sedang digunakan aplikasi lain, kemudian jalankan:

```bat
.venv\Scripts\activate
python main.py
```

Game akan membuka jendela berukuran `800 x 600` dan menampilkan citra webcam
secara terbalik horizontal agar gerakan terasa seperti bercermin.

## Kontrol

| Tombol | Fungsi |
| --- | --- |
| `Space` | Menjeda/melanjutkan permainan, atau menutup layar Level Up |
| `Esc` | Keluar dari permainan |
| Menunjukkan jari telunjuk | Menggerakkan kursor dan menebas buah |

## Cara Bermain

1. Berdiri atau duduk di depan webcam dengan tangan terlihat jelas.
2. Arahkan ujung jari telunjuk ke buah yang bergerak.
3. Gerakkan jari melewati area buah untuk memotongnya.
4. Setiap buah yang terpotong memberikan 10 poin.
5. Buah yang jatuh keluar layar tanpa terpotong mengurangi skor 5 poin.
6. Pantau skor dan level di kiri atas layar.
7. Saat skor mencapai kelipatan 150, layar **LEVEL UP!** muncul, permainan
   berhenti sementara dan semua buah dibersihkan. Tekan `Space` untuk lanjut.

Tidak ada sistem nyawa, sehingga permainan tidak pernah berakhir; skor bisa
menjadi negatif. Level hanya naik dan tidak turun walau skor berkurang.

## Konfigurasi

Pengaturan utama terdapat di [`config.py`](config.py):

| Konstanta | Nilai awal | Keterangan |
| --- | ---: | --- |
| `WIDTH` | `800` | Lebar jendela dan frame kamera |
| `HEIGHT` | `600` | Tinggi jendela dan frame kamera |
| `FPS` | `30` | Batas frame permainan |
| `LOWER_COLOR` / `UPPER_COLOR` | HSV | Rentang warna; saat ini belum digunakan oleh tracker |
| `MIN_CONTOUR_AREA` | `400` | Parameter area kontur; saat ini belum digunakan |
| `MAX_TRAIL_LEN` | `8` | Panjang maksimum jejak jari |
| `TIME_PER_LEVEL` | `30` | Waktu per level (detik); saat ini belum digunakan |
| `SPAWN_INTERVAL` | `10` | Interval dasar kemunculan buah dalam frame (lihat catatan di bawah) |
| `POINTS_PER_LEVEL` | `150` | Poin yang diperlukan untuk naik level |
| `FRUIT_RADIUS` | `35` | Radius buah |
| `GRAVITY` | `0.6` | Gravitasi buah |

Indeks kamera dapat diubah di [`main.py`](main.py) pada bagian:

```python
tracker = ColorTracker(camera_index=0)
```

Gunakan `camera_index=1` atau indeks lain jika webcam yang diinginkan bukan
perangkat kamera default.

## Struktur Proyek

```text
Comp Vis Fruit Ninja/
├── main.py          # Loop permainan, input keyboard, rendering, dan skor
├── cv_tracker.py    # Akses webcam dan pelacakan ujung jari dengan MediaPipe
├── fruit.py         # Logika gerak dan gambar buah
├── config.py        # Konfigurasi tampilan, computer vision, dan gameplay
├── utils.py         # Irisan garis tebasan dengan buah & efek suara level up
├── requirements.txt # Daftar dependensi Python
└── README.md        # Dokumentasi proyek
```

## Dependensi

Dependensi proyek didefinisikan di [`requirements.txt`](requirements.txt):

- `pygame` untuk jendela, input, dan rendering game.
- `opencv-python` untuk membaca serta memproses frame webcam.
- `mediapipe` untuk mendeteksi landmark tangan.
- `numpy` untuk operasi array, ketebalan jejak, dan sintesis suara level up.
- `pymunk` tercantum sebagai dependensi proyek, meskipun logika fisika saat
  ini diimplementasikan langsung di `fruit.py`.

## Pemecahan Masalah

### Kamera tidak terbuka atau game langsung berhenti

- Pastikan webcam terhubung dan memiliki izin akses.
- Tutup aplikasi lain yang sedang memakai webcam.
- Coba ubah `camera_index` di `main.py`.
- Pastikan game dijalankan dari virtual environment yang sudah memasang
  semua dependensi.

### Tangan tidak terdeteksi

- Pastikan telapak dan ujung jari terlihat penuh di kamera.
- Gunakan pencahayaan yang cukup dan hindari latar belakang yang terlalu
  ramai.
- Jaga jarak tangan agar tetap berada di dalam frame.

### Instalasi MediaPipe atau OpenCV gagal

- Gunakan Python 3.11 sesuai persyaratan proyek.
- Pastikan virtual environment aktif sebelum menjalankan `pip install`.
- Perbarui pip dengan `python -m pip install --upgrade pip`, lalu ulangi
  instalasi dependensi.

## Catatan Pengembangan

Program utama dijalankan dari `main.py`. Setiap frame diproses oleh
`ColorTracker`, kemudian posisi dua titik terakhir pada jejak jari diperiksa
terhadap lingkaran buah oleh `line_intersects_circle` di `utils.py`.
Perubahan aturan skor, level, atau fisika buah dapat dilakukan di
`config.py` dan `fruit.py`.

Level dihitung sebagai `skor // POINTS_PER_LEVEL + 1`. Saat level naik,
`main.py` menandai `is_level_up`, membersihkan buah, memulai animasi konfeti,
dan memainkan suara dari `make_levelup_sound` (arpeggio C-E-G-C).

Catatan: interval kemunculan buah dihitung `max(12, SPAWN_INTERVAL - (level - 1) * 4)`,
sehingga karena `SPAWN_INTERVAL` bernilai 10, hasilnya selalu 12 frame. Tingkat
kesulitan antarlevel saat ini hanya berasal dari kecepatan lontaran buah
(`fruit.py`).
