# 🍕 QR Menu AI - AI-Powered Restaurant Menu System

AI güçlü, QR kod tabanlı restoran menü ve sipariş yönetim sistemi. Streamlit ile geliştirilmiş modern bir web uygulaması.

## 🔥 Latest Updates (v2.0.1 - Oct 7, 2025)

✅ **Bug Fixes Completed**
- Fixed database query errors in Menu & Table Management
- Improved AI Assistant UI (chat input moved to top)
- Enhanced mobile compatibility with auto-test script
- Fixed quick delete refresh errors

📱 **Mobile Support**
- New mobile test script: `mobile_test.ps1`
- Automatic IP detection and QR code generation
- Detailed mobile testing guide: [MOBILE_TEST_GUIDE.md](MOBILE_TEST_GUIDE.md)

📚 **Documentation**
- Bug fix summary: [BUGFIX_SUMMARY.md](BUGFIX_SUMMARY.md)
- Mobile testing: [MOBILE_TEST_GUIDE.md](MOBILE_TEST_GUIDE.md)
- Quick start: [QUICKSTART.md](QUICKSTART.md)

---

## ✨ Özellikler

### Müşteri Tarafı
- 🤖 **AI Menü Asistanı**: Doğal dil ile sipariş ve öneri alma
- 📱 **QR Kod Entegrasyonu**: Masa bazlı oturum yönetimi
- 🛒 **Akıllı Sepet**: Real-time fiyat hesaplama
- 🌱 **Filtreler**: Vejetaryen, vegan, alerjen filtreleme
- 🌐 **Çoklu Dil**: Türkçe/İngilizce desteği
- 💬 **Chat Interface**: AI ile sohbet ederek sipariş

### Admin/Personel Tarafı
- 📊 **Dashboard**: Günlük satış ve istatistikler
- 🏓 **Masa Yönetimi**: CRUD işlemleri, QR kod yönetimi
- 📋 **Sipariş Takibi**: Hazırlanma durumu yönetimi
- 🍽️ **Menü Yönetimi**: Tam CRUD işlemleri (Ekle/Düzenle/Sil)
- � **Kategori Yönetimi**: Kategori CRUD, sıralama, istatistikler
- �📈 **Raporlama**: Excel export, detaylı satış raporları
- 🔔 **Bildirimler**: Real-time sipariş bildirimleri
- 🎨 **Tema Özelleştirme**: Marka uyumlu görünüm

### AI Özellikleri
- 🔍 **RAG (Retrieval-Augmented Generation)**: Akıllı menü araması
- 💡 **Kişiselleştirilmiş Öneriler**: Geçmiş siparişlere göre
- 🥜 **Alerjen Kontrolü**: Otomatik güvenlik kontrolü
- 🌶️ **Akıllı Filtreleme**: Tercih bazlı öneri

## 🏗️ Teknoloji Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain + Ollama (llama3.2)
- **Embedding**: mxbai-embed-large
- **Vector DB**: ChromaDB
- **Database**: SQLite (SQLAlchemy ORM)
- **QR Code**: qrcode + pyzbar
- **Future**: Django + React (Phase 2)

## 📁 Proje Yapısı

```
QRMenuRest/
├── app.py                    # Ana Streamlit uygulaması
├── requirements.txt          # Python bağımlılıkları
├── .env                      # Çevre değişkenleri
├── README.md
│
├── pages/                    # Streamlit sayfaları
│   ├── 1_🍽️_Menu.py
│   ├── 2_🛒_Cart.py
│   ├── 3_💬_AI_Assistant.py
│   ├── 4_📊_Admin_Dashboard.py
│   ├── 5_🏓_Table_Management.py
│   ├── 6_📈_Reports.py
│   ├── 7_🔔_Notifications.py
│   ├── 8_🎨_Theme_Settings.py
│   └── 9_📂_Category_Management.py
│
├── ai/                       # AI modülleri
│   ├── rag_engine.py         # RAG sistemi
│   ├── assistant.py          # AI asistan
│   └── prompts.py            # Prompt templates
│
├── database/                 # Veritabanı
│   ├── models.py             # SQLAlchemy modelleri
│   ├── db_manager.py         # CRUD işlemleri
│   └── init_data.py          # Veri yükleme
│
├── utils/                    # Yardımcı modüller
│   ├── qr_utils.py           # QR kod yönetimi
│   ├── session_manager.py    # Oturum yönetimi
│   └── notification_manager.py # Bildirim sistemi
│
├── data/                     # Veri dosyaları
│   ├── menu_items.csv        # Menü ürünleri
│   └── realistic_restaurant_reviews.csv
│
└── static/                   # Statik dosyalar
    ├── images/               # Yemek görselleri
    ├── qr_codes/             # QR kodlar
    └── css/                  # Custom CSS
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Ollama
- Git

### 1. Ollama Kurulumu

```powershell
# Windows için Ollama indir: https://ollama.ai/download
# Kurulumdan sonra modelleri indir:
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### 2. Proje Kurulumu

```powershell
# Repository'yi klonla
git clone https://github.com/yourusername/QRMenuRest.git
cd QRMenuRest

# Virtual environment oluştur
python -m venv venv
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. Veritabanı Başlatma

```powershell
# Veritabanını ve örnek verileri oluştur
python database/init_data.py
```

### 4. QR Kodları Oluştur

```powershell
# Tüm masalar için QR kodları oluştur
python utils/qr_utils.py
```

### 5. Uygulamayı Başlat

```powershell
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresini açın.

## 🎯 Kullanım

### Müşteri İçin
1. Masadaki QR kodu tarayın (veya test için masa numarası girin)
2. Menüyü görüntüleyin veya AI asistana sorun
3. Ürünleri sepete ekleyin
4. Siparişi onaylayın

### Admin/Personel İçin
1. Ana sayfadan "Admin/Personel Girişi"ne tıklayın
2. Dashboard'dan günlük istatistikleri görün
3. Masa durumlarını yönetin
4. Siparişleri takip edin

## 📝 Örnek AI Sorguları

```
"Vejetaryen pizzanız var mı?"
"100 TL altında ne yiyebilirim?"
"Fıstık alerjim var, ne önerirsiniz?"
"Acı seven birine ne önerirsiniz?"
"En popüler ürünleriniz neler?"
"Çocuklar için ne uygun?"
```

## 🔧 Yapılandırma

`.env` dosyasını düzenleyerek ayarları değiştirebilirsiniz:

```env
# Restoran Bilgileri
RESTAURANT_NAME="La Pizza Bella"
RESTAURANT_PHONE="+90 555 123 4567"

# AI Ayarları
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=mxbai-embed-large
VECTOR_DB_PATH=./chrome_langchain_db

# Veritabanı
DATABASE_URL=sqlite:///./restaurant.db

# Uygulama
DEBUG_MODE=True
MAX_TABLES=20
DEFAULT_LANGUAGE=tr
```

## 🛠️ Geliştirme

### Test Modunda Çalıştırma

```powershell
# Debug mode
$env:DEBUG_MODE="True"
streamlit run app.py
```

### Veritabanını Sıfırlama

```python
from database.models import drop_all_tables, init_db

drop_all_tables()  # Tüm tabloları sil
init_db()          # Yeniden oluştur
```

### Vector DB'yi Yeniden Oluşturma

```python
from ai.rag_engine import get_rag_engine

engine = get_rag_engine()
engine.rebuild_index()
```

## 📈 Roadmap

### Phase 1 - MVP (Completed ✅)
- [x] Temel menü görüntüleme
- [x] AI asistan entegrasyonu
- [x] QR kod sistemi
- [x] Sipariş yönetimi
- [x] Masa yönetimi

### Phase 2 - Django Migration (Planned)
- [ ] Django REST API
- [ ] React frontend
- [ ] WebSocket real-time updates
- [ ] Payment integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics

### Phase 3 - Advanced Features
- [ ] Voice ordering
- [ ] Image recognition for dishes
- [ ] Loyalty program
- [ ] Multi-restaurant support
- [ ] Kitchen display system

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👥 Ekip

- **AI & Backend**: [Your Name]
- **Frontend**: [Your Name]
- **Design**: [Your Name]

## 📞 İletişim

- Email: info@lapizzabella.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Teşekkürler

- LangChain team
- Ollama team
- Streamlit team
- Open source community

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
