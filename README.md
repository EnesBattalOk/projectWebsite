# Okul Proje Haberleri Platformu

Bu proje, okulların yürüttüğü farklı projeleri ve bu projelerle ilgili haberleri tek bir platformda toplamanızı sağlar.

## Özellikler
- **Çoklu Proje Yönetimi:** İstediğiniz kadar proje oluşturun.
- **Haber Akışı:** Her proje için ayrı haberler/güncellemeler paylaşın.
- **Admin Paneli:** Projeleri ve haberleri kolayca yönetin.
- **Aktif Proje Seçimi:** Ana sayfada hangi projenin varsayılan olarak gösterileceğini seçin.
- **Modern Tasarım:** Şık, modern ve mobil uyumlu kullanıcı arayüzü.

## Kurulum
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install flask flask-sqlalchemy
   ```
2. Uygulamayı çalıştırın:
   ```bash
   python app.py
   ```
3. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

## Admin Erişimi
Uygulama içinde `/admin` rotasına giderek projeleri yönetmeye başlayabilirsiniz.
- Yeni Proje Ekle
- Projeyi "Aktif" (Varsayılan) olarak işaretle
- Proje bazlı haber ekle/sil
- Proje detaylarını (logo, kapak resmi, açıklama) düzenle

## Teknoloji Yığını
- **Backend:** Python Flask
- **Veritabanı:** SQLite & SQLAlchemy
- **Frontend:** Jinja2 Templates, Vanilla CSS (Modern CSS3), Vanilla JS
- **İkonlar:** FontAwesome 6
- **Font:** Google Fonts (Outfit)
