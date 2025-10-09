# 🚀 QR Menu AI v2.0 - Hızlı Başlangıç

## 📦 5 Dakikada Kurulum

### Adım 1: Gerekli Yazılımları Kur (Bir Kerelik)

```powershell
# 1. Ollama'yı indir ve kur
# https://ollama.ai/download

# 2. AI modellerini indir
ollama pull llama3.2
ollama pull mxbai-embed-large

# 3. Python 3.8+ kurulu olduğunu kontrol et
python --version
```

### Adım 2: Projeyi Kur

```powershell
# Repository'yi klonla veya zip'ten aç
cd QRMenuRest

# Virtual environment oluştur (önerilen)
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Bağımlılıkları kur
pip install -r requirements.txt
```

### Adım 3: Veritabanını Hazırla

```powershell
# Otomatik kurulum scripti çalıştır
python database/init_data.py
```

### Adım 4: Uygulamayı Başlat

```powershell
streamlit run app.py
```

🎉 **Hazır!** Tarayıcınızda http://localhost:8501 açılacak.

---

## 🧪 Test Etmek İçin

### Müşteri Deneyimi
1. Ana sayfada "Test Modu" kullan
2. Masa numarası: 1-20 arası herhangi biri
3. Menüden ürün ekle → AI asistanla konuş → Sipariş ver

### Admin Paneli
1. Sidebar'da "🔐 Admin/Personel Girişi"
2. Sayfalar:
   - **📊 Admin Dashboard**: Sipariş takibi, metrikler
   - **🏓 Table Management**: Masa yönetimi
   - **📈 Reports**: Satış raporları
   - **🔔 Notifications**: Bildirimler
   - **🎨 Theme Settings**: Tema özelleştirme

---

## ⚡ Hızlı Komutlar

```powershell
# Uygulamayı başlat
streamlit run app.py

# Veritabanını sıfırla
rm restaurant.db
python database/init_data.py

# Vector DB'yi yeniden oluştur
python vector.py

# Tüm QR kodları yeniden oluştur
python -c "from utils.qr_utils import generate_all_table_qrs; generate_all_table_qrs()"
```

---

## 🎨 İlk Özelleştirmeler

### 1. Restaurant Bilgilerini Değiştir
`.env` dosyasını düzenle:
```bash
RESTAURANT_NAME="Senin Restaurant İsmin"
RESTAURANT_PHONE="+90 555 XXX XXXX"
RESTAURANT_ADDRESS="Adresin"
```

### 2. Logo Ekle
1. Admin girişi yap
2. "🎨 Theme Settings" → "Logo ve Marka"
3. Logo dosyasını yükle
4. Kaydet

### 3. Tema Değiştir
1. "🎨 Theme Settings" → "Renkler"
2. Hazır temalardan birini seç veya özel renkler belirle
3. "Önizleme ve Kaydet" → "Temayı Kaydet"

---

## 📧 Email Bildirimleri Kurulumu (Opsiyonel)

### Gmail ile (Önerilen)

1. **App Password Oluştur**:
   - Gmail hesabına gir
   - Güvenlik → 2 Adımlı Doğrulama → Uygulama Şifreleri
   - "Uygulama Şifresi Oluştur"
   - 16 karakterli şifreyi kopyala

2. **.env Dosyasını Güncelle**:
```bash
EMAIL_ENABLED=true
EMAIL_FROM=senin-email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  # App Password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

3. **Test Et**:
   - Bir sipariş oluştur
   - Email'ini kontrol et

---

## 🐛 Sorun Giderme

### Ollama Bağlantı Hatası
```powershell
# Ollama'nın çalıştığını kontrol et
ollama list

# Modelleri tekrar indir
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Veritabanı Hatası
```powershell
# Veritabanını sıfırla
rm restaurant.db
python database/init_data.py
```

### Port Zaten Kullanımda
```powershell
# Farklı port kullan
streamlit run app.py --server.port 8502
```

### Vector DB Hatası
```powershell
# Vector DB'yi sil ve yeniden oluştur
rm -r chrome_langchain_db
python vector.py
```

---

## 📱 Mobil Test

### Yerel Ağda Test (Aynı WiFi)

1. Bilgisayarının IP adresini bul:
```powershell
ipconfig  # Windows
# ifconfig  # Mac/Linux
```

2. Streamlit'i network modda başlat:
```powershell
streamlit run app.py --server.address 0.0.0.0
```

3. Telefondan eriş:
```
http://[BILGISAYAR-IP]:8501
```

Örnek: `http://192.168.1.100:8501`

---

## 🎯 Önerilen İlk Adımlar

### 1. Menüyü Özelleştir
- Admin → Dashboard → "Menü Yönetimi"
- Mevcut ürünleri düzenle veya yenilerini ekle

### 2. Masa Sayısını Ayarla
- Admin → Table Management
- İhtiyaç yoksa bazı masaları sil
- Veya yeni masalar ekle

### 3. QR Kodları Yazdır
- `static/qr_codes/` klasöründeki PNG dosyaları
- Her masaya bir QR kod yazdır

### 4. Test Siparişleri Oluştur
- Test moduyla farklı masalardan sipariş ver
- Dashboard'da takip et
- Raporları kontrol et

### 5. Temayı Markana Uyarla
- Logo yükle
- Renk paletini seç
- Restaurant bilgilerini güncelle

---

## 📚 Ekstra Kaynaklar

- **Detaylı Dokümantasyon**: `README.md`
- **Bonus Özellikler**: `BONUS_FEATURES.md`
- **Özellik Karşılaştırması**: `FEATURE_COMPARISON.md`
- **Streamlit Docs**: https://docs.streamlit.io/

---

## 💡 Pro İpuçları

1. **Vector DB**: Her menü değişikliğinde otomatik güncellenir (manuel işlem gereksiz)

2. **Admin Modu**: Sidebar'daki butona basınca aktif olur, tekrar basınca kapanır

3. **Bildirimler**: Sidebar'da real-time görünür, bildirim sayfasından detaylı görüntüle

4. **Raporlar**: "Hızlı Seçim" kullan, export etmeden önce önizle

5. **Tema**: Değişikliklerini JSON'a export et, backup için sakla

---

## 🆘 Yardım

Sorun yaşıyorsan:
1. Terminal çıktısını kontrol et
2. `QUICKSTART.md` dosyasına bak
3. GitHub Issues açabilirsin
4. Logs: `.streamlit/` klasöründe

---

## ✅ Kontrol Listesi

Kurulum tamamlandı mı?

- [ ] Ollama kuruldu ve modeller indirildi
- [ ] Python bağımlılıkları kuruldu
- [ ] Veritabanı oluşturuldu (35+ ürün var mı?)
- [ ] Uygulama başarıyla çalışıyor
- [ ] Test siparişi verebildin
- [ ] Admin paneline girebildin
- [ ] QR kodlar oluşturuldu

Özelleştirme tamamlandı mı?

- [ ] Restaurant bilgileri güncellendi
- [ ] Logo yüklendi
- [ ] Tema seçildi
- [ ] Menü özelleştirildi
- [ ] Masa sayısı ayarlandı

Bonus özellikler test edildi mi?

- [ ] Rapor oluşturuldu ve export edildi
- [ ] Bildirimler çalışıyor
- [ ] Tema değişikliği test edildi
- [ ] CRUD işlemleri denendi

---

## 🎊 Başarıyla Kuruldu!

Artık restaurant'ında kullanmaya hazırsın!

**Sonraki Adımlar**:
- Production deployment (Django)
- Mobil uygulama (React Native)
- Payment entegrasyonu
- Analytics dashboard

**Keyifli Kullanımlar!** 🍕🚀
