# 📂 Kategori Yönetimi - Kullanım Kılavuzu

## 🎯 Genel Bakış

Kategori Yönetimi sayfası, menü kategorilerinizi organize etmenizi ve yönetmenizi sağlar. Bu sayfa ile kategorileri ekleyebilir, düzenleyebilir, silebilir ve detaylı istatistikleri görüntüleyebilirsiniz.

## 📍 Erişim

**Yol 1**: Admin Dashboard → "📂 Kategori Yönetimi" butonu  
**Yol 2**: Direkt URL: `/9_📂_Category_Management`

## ✨ Özellikler

### 1. 📋 Kategori Listesi

**Üst Panel - İstatistikler**:
- 📂 Toplam Kategori
- 🍽️ Toplam Ürün (tüm kategorilerde)
- ✅ Aktif Kategori (ürün içeren)
- 📭 Boş Kategori

**Kategori Kartları**:
- Kategori adı ve ikonu
- Açıklama
- Ürün sayısı (aktif/toplam)
- Sıra numarası (inline düzenleme)
- Ürün listesi (genişletilebilir)

**Sıralama Seçenekleri**:
- Sıra Numarası (varsayılan)
- İsim (A-Z)
- İsim (Z-A)
- Ürün Sayısı

### 2. ➕ Yeni Kategori Ekle

**Form Alanları**:

**Sol Kolon**:
- **Kategori Adı** * (zorunlu): Türkçe isim
- **İkon**: Kategoriyi temsil eden emoji (varsayılan: 🍽️)
- **Açıklama**: Kısa kategori açıklaması

**Sağ Kolon**:
- **Kategori Adı (İngilizce)**: İngilizce isim (opsiyonel)
- **Sıra Numarası**: Menüde görünme sırası (0-100)
- **Aktif**: Kategoriyi menüde göster/gizle

**Özellikler**:
- ✅ Duplicate kontrolü (aynı isimde kategori eklenemez)
- ✅ Otomatik sıra numarası ataması
- ✅ Vector DB otomatik güncelleme
- ✅ Başarı bildirimi ve confetti animasyonu

### 3. ✏️ Kategori Düzenle

**İşlem Adımları**:
1. Dropdown'dan kategori seçin
2. Form alanlarını güncelleyin
3. "💾 Güncelle" butonuna tıklayın

**Düzenlenebilir Alanlar**:
- Kategori adı (TR/EN)
- İkon
- Açıklama
- Sıra numarası
- Aktif durumu

**Bilgiler**:
- Mevcut ürün sayısı gösterimi
- Aktif ürün sayısı
- Duplicate kontrolü (diğer kategorilerle)

### 4. 🗑️ Kategori Sil

**Güvenlik Özellikleri**:
- ⚠️ **Sadece boş kategoriler silinebilir**
- Ürün içeren kategoriler için uyarı mesajı
- "SİL" onay metni zorunluluğu
- Çoklu seçim desteği (toplu silme)

**Kategori Sınıflandırması**:
- 🔒 **Silinemeyen**: Ürün içeren kategoriler
- ✅ **Silinebilir**: Boş kategoriler

**İşlem Adımları**:
1. Silinebilir kategorilerden seçim yapın
2. Onay kutusuna "SİL" yazın
3. "🗑️ Seçilenleri Sil" butonuna tıklayın

### 5. 📊 İstatistikler

**Tablo Görünümü**:
| Kategori | Ürün Sayısı | Aktif Ürün | Toplam Ciro | Sipariş Sayısı | Sıra |
|----------|-------------|------------|-------------|----------------|------|
| 🍕 Pizzalar | 12 | 10 | ₺5,420.00 | 87 | 1 |

**En Başarılı Kategoriler**:
- **💰 Ciro Bazında**: Top 5 kategori (toplam satış)
- **📦 Sipariş Sayısı Bazında**: Top 5 kategori (sipariş adedi)

**Ürün Dağılımı Grafiği**:
ASCII tabanlı bar chart (kategori başına ürün sayısı)

```
🍕 Pizzalar           ████████████████████ 12 ürün
🥗 Salatalar          ████████████ 8 ürün
🍰 Tatlılar           ██████ 4 ürün
```

## 🔧 Kullanım Senaryoları

### Senaryo 1: Yeni Kategori Ekleme
```
Durum: Restorana yeni bir "Vejetaryen" menüsü ekleniyor
Adımlar:
1. "➕ Yeni Kategori" tab'ine git
2. Form doldur:
   - Ad: Vejetaryen Menü
   - İkon: 🌱
   - Açıklama: Et içermeyen lezzetli tarifler
   - Sıra: 3
3. "Kategori Ekle" butonuna tıkla
4. ✅ Kategori eklendi, vector DB güncellendi
```

### Senaryo 2: Kategori Sırasını Değiştirme
```
Durum: "Başlangıçlar" kategorisi en üstte olmalı
Adımlar:
1. "📋 Kategori Listesi" tab'inde kal
2. "Başlangıçlar" kartındaki sıra numarasını 0 yap
3. Otomatik kaydedilir ve sayfa yenilenir
4. ✅ Kategori en üstte görünür
```

### Senaryo 3: Boş Kategori Temizliği
```
Durum: Ürün eklenmemiş 3 eski kategori var
Adımlar:
1. "🗑️ Sil" tab'ine git
2. "✅ Silinebilir Kategoriler" bölümünde 3'ünü seç
3. Onay kutusuna "SİL" yaz
4. "Seçilenleri Sil" butonuna tıkla
5. ✅ 3 kategori temizlendi
```

### Senaryo 4: Kategori İstatistikleri İnceleme
```
Durum: Hangi kategoriler daha çok satılıyor?
Adımlar:
1. "📊 İstatistikler" tab'ine git
2. "💰 Ciro Bazında" bölümüne bak
3. En çok kazandıran kategoriyi görüntüle
4. Tabloda detaylı verileri incele
```

## 💡 İpuçları

### Sıralama
- **0-10**: Premium kategoriler (Özel Menüler, Şef Önerileri)
- **11-20**: Ana kategoriler (Pizzalar, Ana Yemekler)
- **21-30**: Yan kategoriler (Salatalar, İçecekler)
- **31+**: Diğer kategoriler (Tatlılar, Ekstralar)

### İkon Seçimi
Kategori karakterini yansıtan emojiler kullanın:
- 🍕 Pizzalar
- 🥗 Salatalar
- 🍔 Burgerler
- 🍰 Tatlılar
- 🍹 İçecekler
- 🌱 Vejetaryen
- 🌶️ Acılı Yemekler
- ⭐ Özel Menü
- 👨‍🍳 Şef Önerileri

### Kategori İsimlendirme
- **Açık ve net**: "Başlangıçlar" ✅ vs "Diğer" ❌
- **Tanımlayıcı**: "Glutensiz Ürünler" ✅
- **Kısa**: "Pizzalar" ✅ vs "Pizza ve İtalyan Makarnalar" ❌
- **Tutarlı**: Tüm kategoriler aynı dil ve stilde

## ⚠️ Dikkat Edilmesi Gerekenler

### 1. Kategori Silme
- ❌ **Ürün içeren kategori silinemez**
- ✅ Önce ürünleri başka kategoriye taşıyın veya silin
- ⚠️ Silme işlemi geri alınamaz

### 2. Kategori İsimleri
- 🔒 Aynı isimde iki kategori olamaz
- 📝 Düzenleme sırasında da duplicate kontrolü yapılır

### 3. Sıra Numaraları
- 🔢 Aynı sıra numarası kullanılabilir (sistem sıralar)
- 📊 Menü sayfasında sıralı görünür
- 🔄 İstediğiniz zaman değiştirebilirsiniz

### 4. Vector DB Senkronizasyonu
- 🤖 Her kategori değişikliğinde AI sistemi güncellenir
- ⏱️ Bu işlem birkaç saniye sürebilir
- ✅ Tamamlandığında bildirim alırsınız

## 🔗 İlgili Sayfalar

- **🍽️ Menü Yönetimi**: Kategorilere ürün ekleyin
- **📊 Admin Dashboard**: Genel kategori istatistikleri
- **📈 Raporlar**: Kategori bazlı satış raporları
- **🏓 Masa Yönetimi**: Sipariş takibi

## 📊 Performans Metrikleri

Her kategori için izlenen metrikler:
- **Ürün Sayısı**: Toplam ürün adedi
- **Aktif Ürün**: Mevcut satışta olan ürünler
- **Toplam Ciro**: Bu kategoriden kazanılan toplam gelir
- **Sipariş Sayısı**: Kaç kez sipariş edildi
- **Ortalama Sipariş Değeri**: Ciro / Sipariş Sayısı

## 🎨 Görsel Rehber

### Kategori Kartı Yapısı
```
┌─────────────────────────────────────────────┐
│ 🍕 Pizzalar                    Ürün: 12     │
│ İtalyan usulü hamur işleri      ✅ 10 aktif │
│                                              │
│ Sıra: [2]                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ 📦 Ürünleri Görüntüle (12 adet)        │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 🚀 Gelecek Özellikler (Planlanan)

- [ ] Kategori görseli yükleme
- [ ] Alt kategori desteği (Tree yapısı)
- [ ] Kategori renk kodlama
- [ ] Drag & drop sıralama
- [ ] Kategori bazlı indirim tanımlama
- [ ] Zaman bazlı kategori görünürlüğü (Kahvaltı/Öğle/Akşam)
- [ ] Kategori etiketleri (tags)
- [ ] Kategori şablonları (Templates)

## ❓ Sık Sorulan Sorular

**S: Kategori silindiğinde ürünler ne olur?**  
C: Ürün içeren kategori silinemez. Önce ürünleri silmeli veya başka kategoriye taşımalısınız.

**S: Kategori sırası neden önemli?**  
C: Menü sayfasında kategoriler bu sıraya göre görünür. Önce gösterilmesini istediğiniz kategorilere düşük numara verin.

**S: İki kategori aynı sıra numarasına sahip olabilir mi?**  
C: Evet, sistem otomatik olarak sıralar. Ancak net kontrol için farklı numaralar kullanmanız önerilir.

**S: Kategori eklediğimde AI asistan hemen öğrenir mi?**  
C: Evet, kategori eklendikten sonra vector DB otomatik güncellenir ve AI asistan yeni kategoriyi bilir.

**S: Kategori ikonunu nasıl değiştiririm?**  
C: "✏️ Düzenle" tab'inden kategoriyi seçin ve ikon alanına yeni emoji yapıştırın.

**S: İngilizce isim zorunlu mu?**  
C: Hayır, opsiyoneldir. Sadece çok dilli destek istiyorsanız ekleyin.

---

**📘 Daha fazla bilgi için**: README.md, BONUS_FEATURES.md  
**🆘 Destek**: GitHub Issues  
**📅 Son Güncelleme**: 2024 - QR Menu AI v2.0
