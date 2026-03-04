#!/bin/bash

# --- PythonAnywhere Otomatik Güncelleme Scripti ---
# Bu dosyayı PythonAnywhere terminalinde 'sh update.sh' diyerek çalıştırın.

echo "--- 🔄 Güncelleme Başlatılıyor... ---"

# 1. GitHub'dan son değişiklikleri çek (Veritabanına dokunmaz)
echo "1. GitHub'dan kodlar çekiliyor..."
git pull origin main

# 2. Virtualenv aktif et ve kütüphaneleri güncelle
# NOT: Buradaki 'venv' kısmını PythonAnywhere'deki sanal ortam adınızla değiştirin (genelde venv olur)
echo "2. Kütüphaneler kontrol ediliyor..."
source venv/bin/activate
pip install -r requirements.txt

# 3. Veritabanı şemasını güncelle (Eğer yeni sütun eklendiyse)
echo "3. Veritabanı şeması kontrol ediliyor..."
python migrate_db.py

# 4. Web sunucusu yeniden başlatılıyor (Reload)...
# GitHub Repo: https://github.com/EnesBattalOk/projectWebsite.git
echo "4. Web sunucusu yeniden başlatılıyor (Reload)..."
touch /var/www/ourprojects_pythonanywhere_com_wsgi.py

echo "--- ✅ GÜNCELLEME TAMAMLANDI! Web siteniz şu an yayında. ---"
