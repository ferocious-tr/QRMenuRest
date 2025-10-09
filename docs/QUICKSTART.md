# 🚀 Hızlı Başlangıç Rehberi

## ⚡ Hızlı Kurulum (5 Dakika)

### 1. Gereksinimleri Kontrol Edin

✅ Python 3.8+ yüklü olmalı
✅ Ollama yüklü olmalı ([İndir](https://ollama.ai/download))

### 2. Kurulum Komutları

```powershell
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ollama modellerini indir
ollama pull llama3.2
ollama pull mxbai-embed-large

# 3. Veritabanını oluştur
python database/init_data.py

# 4. QR kodları oluştur (opsiyonel)
python utils/qr_utils.py

# 5. Uygulamayı başlat
streamlit run app.py
```

### VEYA Otomatik Kurulum

```powershell
# PowerShell ile otomatik kurulum
.\setup.ps1
```

## 🎮 İlk Kullanım

### Müşteri Olarak Test

1. Tarayıcıda `http://localhost:8501` açın
2. Masa numarası girin (örn: 1)
3. Menüyü inceleyin
4. AI Asistan ile konuşun
5. Ürün ekleyin ve sipariş verin

### Admin Olarak Test

1. Ana sayfada "Admin/Personel Girişi"ne tıklayın
2. Dashboard'u inceleyin
3. Masa durumlarını görün
4. Siparişleri takip edin

## 💡 Örnek AI Sorguları

```
"Vejetaryen pizzanız var mı?"
"100 TL altında ne yiyebilirim?"
"Fıstık alerjim var, ne önerirsiniz?"
"Acı seven birine ne önerirsiniz?"
"En popüler ürünleriniz neler?"
```

## 🐛 Sorun Giderme

### Ollama Bağlantı Hatası
```powershell
# Ollama servisinin çalıştığından emin olun
ollama list
```

### Import Hatası
```powershell
# Sanal ortamı aktifleştirin
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Veritabanı Hatası
```powershell
# Veritabanını sıfırlayın
python
>>> from database.models import drop_all_tables, init_db
>>> drop_all_tables()
>>> init_db()
>>> exit()
python database/init_data.py
```

### Port Zaten Kullanımda
```powershell
# Farklı port kullanın
streamlit run app.py --server.port 8502
```

## 📊 Test Verileri

Sistem otomatik olarak şunları oluşturur:
- 7 kategori (Pizzalar, Başlangıçlar, Ana Yemekler, vb.)
- 35+ menü ürünü
- 20 masa
- Örnek yorumlar

## 🔧 Yapılandırma

`.env` dosyasını düzenleyin:

```env
RESTAURANT_NAME="Kendi Restoranınız"
OLLAMA_MODEL=llama3.2
MAX_TABLES=20
DEFAULT_LANGUAGE=tr
```

## 📱 QR Kod Kullanımı

QR kodlar `static/qr_codes/` klasöründe oluşturulur:
- `table_1.png` - Masa 1 için QR kod
- `table_2.png` - Masa 2 için QR kod
- vb.

Her QR kod şu URL'yi içerir: `http://localhost:8501/?table=N`

## 🎯 Sonraki Adımlar

1. ✅ Uygulamayı test edin
2. 📝 Menüyü özelleştirin (data/menu_items.csv)
3. 🎨 Yemek görselleri ekleyin (static/images/)
4. 🌐 Canlıya alın (deployment)
5. 📱 Gerçek QR kodları yazdırın

## 📞 Yardım

Sorun mu yaşıyorsunuz?
- README.md dosyasına bakın
- GitHub Issues'da sorun açın
- Toplulukla iletişime geçin

---

**İyi Kullanımlar! 🍕**
