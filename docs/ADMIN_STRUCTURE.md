# Admin Panel Yapısı - QR Menu AI v2.0

## 📁 Dizin Yapısı

```
QRMenuRest/
├── admin.py                              # Admin giriş sayfası (http://localhost:8501/admin)
├── app.py                                # Müşteri ana sayfası (http://localhost:8501)
├── pages/                                # Müşteri sayfaları
│   ├── 1_🍽️_Menu.py                     # Menü görüntüleme
│   ├── 2_🛒_Cart.py                      # Sepet ve sipariş
│   └── 3_💬_AI_Assistant.py              # AI asistan
│
└── pages/admin/                          # Admin sayfaları (Yetki korumalı)
    ├── 1_📊_Dashboard.py                 # Admin kontrol paneli
    ├── 2_🏓_Table_Management.py          # Masa yönetimi
    ├── 3_📈_Reports.py                   # Raporlar ve analizler
    ├── 4_🔔_Notifications.py             # Bildirim merkezi
    ├── 5_🎨_Theme_Settings.py            # Tema ayarları
    └── 6_📂_Category_Management.py       # Kategori yönetimi
```

## 🔐 Giriş ve Yetkilendirme

### Admin Girişi
- **URL:** http://localhost:8501/admin
- **Varsayılan Kullanıcı:** admin
- **Varsayılan Şifre:** admin123

### Güvenlik Özellikleri
- ✅ Session tabanlı kimlik doğrulama
- ✅ Sayfa bazlı yetki kontrolü
- ✅ Otomatik yönlendirme (yetkisiz erişim)
- ✅ "Beni Hatırla" özelliği

## 🚀 Kullanım

### Müşteri Erişimi
1. Tarayıcıda `http://localhost:8501` adresini aç
2. Masa QR kodunu tarat veya masa seç
3. Menüden ürün ekle, sipariş ver

### Admin Erişimi
1. Tarayıcıda `http://localhost:8501/admin` adresini aç
2. Kullanıcı adı ve şifre ile giriş yap
3. Dashboard üzerinden tüm işlemleri yönet

## 📊 Admin Panel Özellikleri

### Dashboard (1_📊_Dashboard.py)
- **Gerçek zamanlı istatistikler:** Günlük ciro, sipariş sayısı, aktif siparişler
- **Aktif sipariş yönetimi:** Durum güncelleme, sipariş takibi
- **Popüler ürünler:** En çok satılan ürünler
- **Masa durumu:** Tüm masaların anlık görünümü
- **Menü CRUD:** Ürün ekleme, düzenleme, silme

### Masa Yönetimi (2_🏓_Table_Management.py)
- **Masa grid görünümü:** Tüm masaların görsel takibi
- **Masa CRUD:** Yeni masa ekleme, düzenleme, silme
- **QR kod yönetimi:** Otomatik QR kod oluşturma
- **Sipariş detayları:** Masa bazında sipariş görüntüleme
- **Durum güncelleme:** Müsait, Dolu, Rezerve, Temizleniyor

### Raporlar (3_📈_Reports.py)
- **Satış raporları:** Tarih aralığına göre detaylı satış analizi
- **Ürün performansı:** En çok satan ürünler, kategori bazlı analiz
- **Günlük dağılım:** Günlük sipariş ve ciro grafikleri
- **Export:** Excel ve CSV formatında rapor indirme

### Bildirimler (4_🔔_Notifications.py)
- **Bildirim merkezi:** Tüm bildirimleri görüntüleme
- **Okunmamış takibi:** Okunmamış bildirimleri listeleme
- **Email/SMS ayarları:** Bildirim kanallarını yapılandırma
- **İstatistikler:** Bildirim türleri ve zaman çizelgesi

### Tema Ayarları (5_🎨_Theme_Settings.py)
- **Renk şemaları:** Hazır temalar veya özel renkler
- **Logo yönetimi:** Restaurant logosu yükleme
- **Marka bilgileri:** İsim, slogan, iletişim bilgileri
- **Düzen ayarları:** Menü görünümü, kompakt mod

### Kategori Yönetimi (6_📂_Category_Management.py)
- **Kategori CRUD:** Kategori ekleme, düzenleme, silme
- **Sıralama:** Drag-drop veya sıra numarası ile sıralama
- **İstatistikler:** Kategori bazlı satış ve ciro raporları
- **İkon desteği:** Emoji ile kategori simgeleme

## 🔧 Yapılandırma

### .env Dosyası
```properties
# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

**⚠️ ÖNEMLİ:** Production ortamında mutlaka güçlü şifre kullanın!

### Şifre Değiştirme
1. `.env` dosyasını aç
2. `ADMIN_PASSWORD` değerini değiştir
3. Uygulamayı yeniden başlat

## 🛡️ Güvenlik Notları

### Üretim Ortamı İçin
- [ ] Güçlü şifre kullan (min. 12 karakter)
- [ ] HTTPS kullan
- [ ] Session timeout ayarla
- [ ] IP kısıtlaması ekle
- [ ] 2FA (İki faktörlü doğrulama) ekle
- [ ] Audit logging ekle

### Geliştirme Ortamı
- ✅ Varsayılan credentials (admin/admin123)
- ✅ HTTP üzerinde çalışma
- ✅ Basit session yönetimi

## 📝 Değişiklik Geçmişi

### v2.0 - Admin Panel Ayrımı (2025-10-07)
- ✅ Admin sayfaları `pages/admin/` klasörüne taşındı
- ✅ Admin giriş sayfası (`admin.py`) oluşturuldu
- ✅ Yetki kontrolü tüm admin sayfalarına eklendi
- ✅ Müşteri sayfalarından admin butonları kaldırıldı
- ✅ Session error fixleri (ID-first pattern) korundu
- ✅ `.env` dosyasına admin credentials eklendi

### v1.0 - İlk Sürüm
- Temel CRUD işlemleri
- QR kod sistemi
- AI asistan entegrasyonu
- Bildirim sistemi

## 🤝 Destek

Sorularınız için:
- 📧 Email: admin@restaurant.com
- 📱 Telefon: +90 555 123 4567
- 🌐 Web: http://localhost:8501

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

**QR Menu AI v2.0** - Modern Restaurant Yönetim Sistemi
