from flask import Flask, render_template, request
import hashlib
import gdown
import difflib
import os

app = Flask(__name__)

# URL file di Google Drive
url = 'https://drive.google.com/file/d/1-ZvvNOyGA8Od-YJFD7glFBez2P-hCqse'
file_path = 'data911.txt'

# Fungsi untuk menghasilkan hash
def generate_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            buffer = f.read()
            hasher.update(buffer)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

# Fungsi untuk membaca isi file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return None

@app.route('/', methods=['GET', 'POST'])  # Menambahkan 'POST' di sini
def index():
    if request.method == 'POST':
        # Unduh file dari Google Drive
        gdown.download(url, file_path, quiet=False)

        # Hasilkan hash dan baca isi file asli
        original_hash = generate_hash(file_path)
        original_content = read_file(file_path)

        if original_hash is None or original_content is None:
            return "Gagal membaca file asli."

        # Mengubah isi file (simulasi modifikasi tidak sah)
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("\nData tambahan.")
        except Exception as e:
            return f"Gagal memodifikasi file: {e}"

        # Hasilkan hash dan baca isi yang dimodifikasi
        modified_hash = generate_hash(file_path)
        modified_content = read_file(file_path)

        if modified_hash is None or modified_content is None:
            return "Gagal membaca file setelah modifikasi."

        # Bandingkan hash
        file_status = "File tidak berubah." if original_hash == modified_hash else "File telah diubah."

        # Tampilkan perbedaan
        diff = difflib.unified_diff(original_content, modified_content, lineterm='')
        differences = '\n'.join(list(diff))

        return render_template('index.html', original_hash=original_hash, modified_hash=modified_hash, 
                               file_status=file_status, differences=differences)

    # Kembalikan tampilan HTML untuk metode GET
    return render_template('index.html', original_hash='', modified_hash='', file_status='', differences='')

if __name__ == '__main__':
    app.run(debug=True)
 #tes