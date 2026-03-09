#!/bin/bash

# --- PythonAnywhere Otomatik Güncelleme Scripti ---
# Bu dosyayı PythonAnywhere terminalinde 'bash update.sh' diyerek çalıştırın.

echo "--- 🔄 Güncelleme Başlatılıyor... ---"

# 1. GitHub'dan son değişiklikleri çek (Resimleri/Uploads klasörünü silmez)
echo "1. GitHub'dan yeni kodlar ve güncel veritabanı çekiliyor..."
git fetch origin
git reset --hard origin/main

# 2. Virtualenv aktif et ve kütüphaneleri güncelle
echo "2. Kütüphaneler kontrol ediliyor..."
. venv/bin/activate 2>/dev/null || true
pip install -r requirements.txt --quiet

# 3. Veritabanı şemasını güncelle (Eğer yeni sütun eklendiyse)
echo "3. Veritabanı şeması kontrol ediliyor..."
python migrate_db.py

# 4. Web sunucusu yeniden başlatılıyor (Reload)...
# GitHub Repo: https://github.com/EnesBattalOk/projectWebsite.git
echo "4. Web sunucusu yeniden başlatılıyor (Reload)..."
touch /var/www/ourprojects_pythonanywhere_com_wsgi.py

echo "--- ✅ GÜNCELLEME TAMAMLANDI! Web siteniz şu an yayında. ---"
