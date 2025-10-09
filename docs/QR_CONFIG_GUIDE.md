# 📱 QR Kod Yapılandırma Rehberi

## 🎯 Özet

QR kodları artık `.env` dosyasındaki ayarlara göre otomatik olarak doğru URL ile oluşturuluyor.

---

## ⚙️ Yapılandırma (.env)

### Üç Mod Destekleniyor:

#### 1️⃣ **Production Mode (Domain Name)**
```env
DOMAIN_NAME=https://yourdomain.com
IP_ADDRESS=
PORT=8501
```
- ✅ Production ortamı için
- ✅ QR kodlar: `https://yourdomain.com/?table=1`
- ✅ HTTPS otomatik eklenir (http:// yoksa)

#### 2️⃣ **Local Network Mode (IP Address)**
```env
DOMAIN_NAME=
IP_ADDRESS=192.168.1.113
PORT=8501
```
- ✅ Yerel ağ test için
- ✅ QR kodlar: `http://192.168.1.113:8501/?table=1`
- ✅ Mobil cihazlardan erişilebilir (aynı WiFi'de)

#### 3️⃣ **Development Mode (Localhost)**
```env
DOMAIN_NAME=
IP_ADDRESS=
PORT=8501
```
- ✅ Geliştirme için
- ✅ QR kodlar: `http://localhost:8501/?table=1`
- ✅ Sadece bilgisayardan erişilebilir

---

## 🚀 Kullanım

### QR Kodları Yeniden Oluşturma

#### Tüm Masalar İçin (21 masa):
```python
from utils.qr_utils import generate_all_table_qrs
generate_all_table_qrs(21)
```

veya terminal'den:
```powershell
python -c "from utils.qr_utils import generate_all_table_qrs; generate_all_table_qrs(21)"
```

#### Tek Masa İçin:
```python
from utils.qr_utils import generate_table_qr
generate_table_qr(5)  # Masa 5 için QR kod
```

#### Özel URL İle:
```python
from utils.qr_utils import generate_table_qr
generate_table_qr(5, base_url="https://myrestaurant.com")
```

---

## 📊 Test

Test script'i ile konfigürasyonu kontrol edin:

```powershell
python test_qr.py
```

**Çıktı Örneği:**
```
======================================================================
QR Code Generation Test
======================================================================

📋 Current Configuration (.env):
   DOMAIN_NAME: (not set)
   IP_ADDRESS: 192.168.1.113
   PORT: 8501

🌐 Auto-detected Base URL: http://192.168.1.113:8501

🔄 Generating test QR code for Table 1...

✅ QR code generated for Table 1
   URL: http://192.168.1.113:8501/?table=1
   File: static/qr_codes\table_1.png
```

---

## 🔄 Senaryo Örnekleri

### Senaryo 1: Geliştirme → Yerel Ağ Testi

1. **Başlangıç** (.env):
   ```env
   DOMAIN_NAME=
   IP_ADDRESS=
   PORT=8501
   ```
   → QR kodlar: `localhost:8501`

2. **Mobil Test İçin** (.env güncelle):
   ```env
   IP_ADDRESS=192.168.1.113
   ```

3. **QR Kodları Yenile**:
   ```powershell
   python -c "from utils.qr_utils import generate_all_table_qrs; generate_all_table_qrs(21)"
   ```
   → QR kodlar: `192.168.1.113:8501` ✅

### Senaryo 2: Yerel Ağ → Production

1. **Test Ortamı** (.env):
   ```env
   DOMAIN_NAME=
   IP_ADDRESS=192.168.1.113
   PORT=8501
   ```

2. **Production'a Geçiş** (.env güncelle):
   ```env
   DOMAIN_NAME=restaurant.yourdomain.com
   IP_ADDRESS=
   PORT=443
   ```

3. **QR Kodları Yenile**:
   ```powershell
   python -c "from utils.qr_utils import generate_all_table_qrs; generate_all_table_qrs(21)"
   ```
   → QR kodlar: `https://restaurant.yourdomain.com/?table=X` ✅

---

## 💡 Önemli Notlar

### Domain Name Kullanırken:
- ✅ HTTPS otomatik eklenir
- ✅ Port belirtmeye gerek yok (standart 443/80 kullanılır)
- ✅ Subdomain desteklenir: `menu.restaurant.com`

### IP Address Kullanırken:
- ✅ HTTP kullanılır
- ✅ Port eklenir: `http://IP:PORT`
- ✅ Mobil cihazlar aynı WiFi'de olmalı

### Localhost Kullanırken:
- ✅ Sadece geliştirme için
- ❌ Mobil cihazlardan erişilemez
- ✅ Hızlı test için ideal

---

## 🔧 Admin Panel'den QR Yenileme

Masa Yönetimi sayfasında (Table Management):
1. Masa düzenleme (Edit) bölümüne gidin
2. "QR Kodu Yeniden Oluştur" checkbox'ını işaretleyin
3. Kaydet butonuna basın

→ QR kod otomatik olarak `.env`'deki ayarlara göre yeniden oluşturulur!

---

## 📱 Mobil Test

QR kodlar doğru URL'lerle oluşturulduktan sonra:

1. **Streamlit'i Başlat**:
   ```powershell
   .\mobile_test.ps1
   ```

2. **QR Kodu Tara** veya URL'yi Gir:
   - iPhone/Android Safari/Chrome
   - Aynı WiFi ağında olun
   - QR kod: `static/qr_codes/table_1.png`

3. **Test Et**:
   - Masa seçimi çalışıyor mu?
   - Menü görüntüleniyor mu?
   - Sipariş verebiliyor mu?

---

## 🎉 Hızlı Başlangıç

### Mobil Test İçin (3 Adım):

1. **.env Dosyasını Güncelle**:
   ```env
   IP_ADDRESS=192.168.1.113  # Kendi IP'nizi yazın
   ```

2. **QR Kodları Yenile**:
   ```powershell
   python -c "from utils.qr_utils import generate_all_table_qrs; generate_all_table_qrs(21)"
   ```

3. **Streamlit'i Başlat ve Test Et**:
   ```powershell
   .\mobile_test.ps1
   ```

**Tamamdır! QR kodlarınız mobil erişim için hazır! 🚀📱**

---

## 📞 Sorun Giderme

### QR Kod Yanlış URL Gösteriyor

1. `.env` dosyasını kontrol edin
2. QR kodları yeniden oluşturun
3. `test_qr.py` ile test edin

### Domain Çalışmıyor

- DNS ayarlarını kontrol edin
- HTTPS sertifikası aktif mi?
- Reverse proxy yapılandırması doğru mu?

### IP Address Değişti

1. Yeni IP'yi `.env`'ye yazın
2. QR kodları yenileyin
3. Streamlit'i yeniden başlatın

---

**Oluşturulma Tarihi**: 7 Ekim 2025  
**Versiyon**: QR Menu AI v2.0.1  
**Son Güncelleme**: QR kod otomasyonu eklendi
