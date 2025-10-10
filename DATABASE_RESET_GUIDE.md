# Database Management Scripts

Bu klasörde database yönetimi için 4 farklı script bulunmaktadır.

## 🚀 Hızlı Başlangıç

### Windows PowerShell (Önerilen)
```powershell
.\db_manager.ps1
```
Menüden seçim yapın ve işleminizi tamamlayın!

### Manuel Python Komutları
```bash
# Reset database
python reset_database.py

# Advanced reset
python reset_database_advanced.py

# Add sample data
python add_sample_data.py
```

---

## 🔧 Scriptler

### 1. `db_manager.ps1` - Ana Menü (Önerilen) 🎯
PowerShell menü scripti. Tüm işlemler için tek tıklama.

**Özellikler:**
- ✨ Kolay kullanımlı menü
- 🎨 Renkli çıktılar
- 🔄 Full reset + sample data seçeneği
- ✅ Python version kontrolü

**Kullanım:**
```powershell
.\db_manager.ps1
```

**Menü Seçenekleri:**
1. 🗑️ Reset Database (Simple)
2. 🔧 Reset Database (Advanced)
3. ➕ Add Sample Data
4. 🔄 Full Reset + Sample Data
5. ❌ Exit

---

### 2. `reset_database.py` - Basit Reset
Tüm database'i sıfırlar. Hızlı ve basit kullanım için.

**Kullanım:**
```bash
python reset_database.py
```

**Ne yapar:**
- ✅ Otomatik backup oluşturur (`restaurant_backup_YYYYMMDD_HHMMSS.db`)
- 🗑️ Tüm siparişleri siler
- 🗑️ Tüm menü öğelerini siler
- 🗑️ Tüm kategorileri siler
- 🗑️ Tüm masaları siler
- 🗑️ Restoran ayarlarını siler
- 🔄 Auto-increment sayaçlarını sıfırlar

**Güvenlik:**
- Onay ister (`YES` yazmanız gerekir)
- Otomatik backup oluşturur

---

### 3. `reset_database_advanced.py` - Gelişmiş Reset
Seçenekli reset işlemi. Sadece istediğiniz kısmı sıfırlayabilirsiniz.

**Kullanım:**
```bash
python reset_database_advanced.py
```

**Seçenekler:**

1. **Reset Everything (Tüm veri)** 🗑️
   - Her şeyi siler

2. **Reset Orders Only (Sadece siparişler)** 📦
   - Menü ve masalar kalır
   - Sadece siparişler silinir

3. **Reset Menu Only (Sadece menü)** 🍽️
   - Siparişler ve masalar kalır
   - Sadece menü öğeleri ve kategoriler silinir

4. **Reset Tables Only (Sadece masalar)** 🏓
   - Menü kalır
   - Masalar silinir (siparişler de silinir)

5. **Reset Orders + Menu** 🔄
   - Sadece masalar kalır
   - Siparişler ve menü silinir

6. **Cancel (İptal)** ❌

**Özellikler:**
- 📊 İşlem öncesi ve sonrası istatistikleri gösterir
- ✅ Otomatik backup oluşturur
- ⚠️ Çift onay ister

---

### 4. `add_sample_data.py` - Test Verisi Ekle ✨
Gerçekçi test verileri oluşturur.

**Kullanım:**
```bash
python add_sample_data.py
```

**Ne ekler:**
- 🏢 Restoran bilgileri
- 📁 5 kategori (Başlangıçlar, Ana Yemekler, Pizza, Tatlılar, İçecekler)
- 🍽️ 13 menü öğesi
- 🏓 10 masa (1-8: 4 kişilik, 9-10: 6 kişilik)
- 📦 Son 7 günden 50-100 sipariş (rastgele)
- ⭐ Rastgele rating'ler (served/paid siparişler için)

**Özellikler:**
- ✅ Mevcut verinin üzerine ekler
- ⚠️ Var olan veri varsa uyarır
- 📊 Özet gösterir

---

## 📋 Kullanım Senaryoları

### Senaryo 1: İlk Kurulum
```powershell
.\db_manager.ps1
# Seçenek 4: Full Reset + Sample Data
```
veya
```bash
python reset_database.py
python add_sample_data.py
```

### Senaryo 2: Sadece siparişleri temizle
```powershell
.\db_manager.ps1
# Seçenek 2: Advanced Reset
# Seçenek 2: Reset Orders Only
```

### Senaryo 3: Daha fazla test verisi ekle
```bash
python add_sample_data.py
# YES yaz (mevcut verinin üzerine ekler)
```

### Senaryo 4: Menüyü yeniden başlat
```bash
python reset_database_advanced.py
# 3 seç (Reset Menu Only)
# Sonra: python database/init_data.py
```

---

## ⚠️ Önemli Notlar

1. **Backup**: Her reset otomatik backup oluşturur
   - Dosya adı: `restaurant_backup_YYYYMMDD_HHMMSS.db`
   - Aynı klasörde saklanır

2. **Geri Alma**: Hata olursa backup'tan geri yükleyebilirsiniz
   ```bash
   # Windows
   copy restaurant_backup_20251009_143025.db restaurant.db
   
   # Linux/Mac
   cp restaurant_backup_20251009_143025.db restaurant.db
   ```

3. **İlk Veri**: Reset sonrası ilk verileri yüklemek için:
   ```bash
   python database/init_data.py
   # veya
   python add_sample_data.py
   ```

4. **Dikkat**: Production ortamında kullanırken çok dikkatli olun!

---

## 🛡️ Güvenlik Özellikleri

✅ Onay mekanizması (YES yazmanız gerekir)
✅ Otomatik backup oluşturma
✅ İşlem öncesi istatistikler
✅ Hata durumunda rollback
✅ Detaylı log mesajları
✅ Python version kontrolü (PowerShell script)

---

## 🔄 Reset Sonrası Adımlar

1. **İlk verileri yükle:**
   ```bash
   python database/init_data.py
   # veya
   python add_sample_data.py
   ```

2. **Uygulamayı başlat:**
   ```bash
   streamlit run app.py
   ```

3. **Admin giriş:**
   - Kullanıcı: admin
   - Şifre: admin123

---

## 📝 Log Örnekleri

### Başarılı Reset:
```
✅ Backup created: restaurant_backup_20251009_143025.db
🗑️  Deleting order items...
   ✓ Order items deleted
🗑️  Deleting orders...
   ✓ Orders deleted
✅ Database reset completed successfully!
```

### Sample Data Oluşturma:
```
🏢 Creating restaurant settings...
   ✓ Restaurant created
📁 Creating categories...
   ✓ 5 categories created
🍽️  Creating menu items...
   ✓ 13 menu items created
✅ Sample data created successfully!
```

### Hata Durumu:
```
❌ Error during reset: ...
💾 Your data is safe in backup: restaurant_backup_20251009_143025.db
```

---

## 🆘 Yardım

Sorun yaşarsanız:
1. Backup dosyasını kontrol edin
2. Database dosyasını backup'tan geri yükleyin
3. Log mesajlarını inceleyin
4. Python version'unu kontrol edin (`python --version`)

---

## 📂 Oluşturulan Dosyalar

```
QRMenuRest/
├── restaurant.db                    # Ana database
├── restaurant_backup_*.db           # Otomatik backup'lar
├── reset_database.py               # Basit reset script
├── reset_database_advanced.py      # Gelişmiş reset script
├── add_sample_data.py              # Test verisi scripti
├── db_manager.ps1                  # Ana menü (PowerShell)
├── reset_db.ps1                    # Basit menü (PowerShell)
└── DATABASE_RESET_GUIDE.md         # Bu dosya
```

---

**Son Güncelleme:** 9 Ekim 2025
Tüm database'i sıfırlar. Hızlı ve basit kullanım için.

**Kullanım:**
```bash
python reset_database.py
```

**Ne yapar:**
- ✅ Otomatik backup oluşturur (`restaurant_backup_YYYYMMDD_HHMMSS.db`)
- 🗑️ Tüm siparişleri siler
- 🗑️ Tüm menü öğelerini siler
- 🗑️ Tüm kategorileri siler
- 🗑️ Tüm masaları siler
- 🗑️ Restoran ayarlarını siler
- 🔄 Auto-increment sayaçlarını sıfırlar

**Güvenlik:**
- Onay ister (`YES` yazmanız gerekir)
- Otomatik backup oluşturur

---

### 2. `reset_database_advanced.py` - Gelişmiş Reset
Seçenekli reset işlemi. Sadece istediğiniz kısmı sıfırlayabilirsiniz.

**Kullanım:**
```bash
python reset_database_advanced.py
```

**Seçenekler:**

1. **Reset Everything (Tüm veri)** 🗑️
   - Her şeyi siler

2. **Reset Orders Only (Sadece siparişler)** 📦
   - Menü ve masalar kalır
   - Sadece siparişler silinir

3. **Reset Menu Only (Sadece menü)** 🍽️
   - Siparişler ve masalar kalır
   - Sadece menü öğeleri ve kategoriler silinir

4. **Reset Tables Only (Sadece masalar)** 🏓
   - Menü kalır
   - Masalar silinir (siparişler de silinir)

5. **Reset Orders + Menu** 🔄
   - Sadece masalar kalır
   - Siparişler ve menü silinir

6. **Cancel (İptal)** ❌

**Özellikler:**
- 📊 İşlem öncesi ve sonrası istatistikleri gösterir
- ✅ Otomatik backup oluşturur
- ⚠️ Çift onay ister

---

## 📋 Örnek Kullanım

### Senaryo 1: Tüm veriyi sıfırla
```bash
python reset_database.py
# YES yaz
```

### Senaryo 2: Sadece siparişleri temizle
```bash
python reset_database_advanced.py
# 2 seç (Reset Orders Only)
# YES yaz
```

### Senaryo 3: Menüyü yeniden başlat
```bash
python reset_database_advanced.py
# 3 seç (Reset Menu Only)
# YES yaz
# Sonra: python database/init_data.py
```

---

## ⚠️ Önemli Notlar

1. **Backup**: Her iki script de otomatik backup oluşturur
   - Dosya adı: `restaurant_backup_YYYYMMDD_HHMMSS.db`
   - Aynı klasörde saklanır

2. **Geri Alma**: Hata olursa backup'tan geri yükleyebilirsiniz
   ```bash
   # Backup'ı kopyala
   copy restaurant_backup_20251009_143025.db restaurant.db
   ```

3. **İlk Veri**: Reset sonrası ilk verileri yüklemek için:
   ```bash
   python database/init_data.py
   ```

4. **Dikkat**: Production ortamında kullanırken çok dikkatli olun!

---

## 🛡️ Güvenlik Özellikleri

✅ Onay mekanizması (YES yazmanız gerekir)
✅ Otomatik backup oluşturma
✅ İşlem öncesi istatistikler
✅ Hata durumunda rollback
✅ Detaylı log mesajları

---

## 🔄 Reset Sonrası Adımlar

1. **İlk verileri yükle:**
   ```bash
   python database/init_data.py
   ```

2. **Uygulamayı başlat:**
   ```bash
   streamlit run app.py
   ```

3. **Admin giriş:**
   - Kullanıcı: admin
   - Şifre: admin123

---

## 📝 Log Örnekleri

### Başarılı Reset:
```
✅ Backup created: restaurant_backup_20251009_143025.db
🗑️  Deleting order items...
   ✓ Order items deleted
🗑️  Deleting orders...
   ✓ Orders deleted
✅ Database reset completed successfully!
```

### Hata Durumu:
```
❌ Error during reset: ...
💾 Your data is safe in backup: restaurant_backup_20251009_143025.db
```

---

## 🆘 Yardım

Sorun yaşarsanız:
1. Backup dosyasını kontrol edin
2. Database dosyasını backup'tan geri yükleyin
3. Log mesajlarını inceleyin

---

**Son Güncelleme:** 9 Ekim 2025
