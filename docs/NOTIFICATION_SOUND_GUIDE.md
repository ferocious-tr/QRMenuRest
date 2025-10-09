# 🔊 Bildirim Ses Sistemi

## Özellikler

Admin Dashboard'a bildirim sesi sistemi eklendi. Yeni sipariş geldiğinde:
- ✅ Görsel bildirim (toast message)
- ✅ **Ses bildirimi** (beep sesi)
- ✅ 10 saniyede bir otomatik kontrol

## Nasıl Çalışır?

### 1. Ses Türleri

`utils/sound_manager.py` dosyasında 5 farklı ses seçeneği var:

#### `play_notification_sound_v1()` - Tek Ton Beep
- Basit, yumuşak beep sesi
- 800 Hz sinüs dalgası
- 0.5 saniye süre

#### `play_notification_sound_v2()` - Çift Ton Beep (Varsayılan)
- İki ardışık beep (1000 Hz → 800 Hz)
- Daha dikkat çekici
- **Şu an kullanılıyor**

#### `play_notification_sound_v3()` - Harici URL
- İnternet bağlantısı gerektirir
- Profesyonel ses dosyası
- Alternatif olarak kullanılabilir

#### `play_success_sound()` - Başarı Sesi
- Üç notadan oluşan melodi (C-E-G akor)
- Pozitif feedback için
- Sipariş tamamlandığında kullanılabilir

#### `play_alert_sound()` - Acil Uyarı
- Üç hızlı beep
- Acil durumlar için
- Daha agresif ses

### 2. Kullanım

```python
from utils.sound_manager import play_notification_sound

# Yeni sipariş geldiğinde
if new_orders_count > 0:
    play_notification_sound()  # Ses çalar
    st.toast("🔔 Yeni sipariş!", icon="🔔")
```

### 3. Ses Değiştirme

`pages/4_📊_Admin_Dashboard.py` dosyasında import satırını değiştirerek farklı ses kullanabilirsiniz:

```python
# Varsayılan (çift ton)
from utils.sound_manager import play_notification_sound

# Tek ton için
from utils.sound_manager import play_notification_sound_v1 as play_notification_sound

# Harici URL için
from utils.sound_manager import play_notification_sound_v3 as play_notification_sound

# Acil uyarı için
from utils.sound_manager import play_alert_sound as play_notification_sound
```

## Teknik Detaylar

### Web Audio API
- Tarayıcı tabanlı ses üretimi
- İnternet bağlantısı gerektirmez
- Tüm modern tarayıcılarda çalışır

### Ses Parametreleri
```javascript
oscillator.frequency.value = 800;  // Frekans (Hz) - ton yüksekliği
oscillator.type = 'sine';          // Dalga tipi: sine, square, triangle
gainNode.gain.value = 0.3;         // Ses seviyesi (0.0-1.0)
duration = 0.5;                    // Süre (saniye)
```

### Özelleştirme

Ses parametrelerini değiştirmek için `utils/sound_manager.py` dosyasını düzenleyin:

```python
# Daha yüksek ses
oscillator.frequency.value = 1200  # Daha tiz

# Daha uzun ses
osc.stop(startTime + 1.0)  # 1 saniye

# Daha yüksek volume
gain.gain.setValueAtTime(0.5, startTime)  # Daha yüksek
```

## Test

Admin Dashboard'a girin ve:
1. Müşteri tarafından bir sipariş oluşturun
2. 10 saniye bekleyin
3. Admin Dashboard yenilendiğinde:
   - 🔔 Toast bildirim görünür
   - 🔊 **Beep sesi duyulur**

## Sorun Giderme

### Ses çalmıyor
1. **Tarayıcı ayarları**: Tarayıcı ses iznini kontrol edin
2. **Sessiz mod**: Bilgisayar sesinin açık olduğundan emin olun
3. **JavaScript**: Tarayıcı konsolunda hata var mı kontrol edin (F12)

### Ses çok yüksek/düşük
`sound_manager.py` dosyasında `gain.gain.setValueAtTime(0.3, ...)` değerini değiştirin:
- `0.1` = Düşük ses
- `0.3` = Orta ses (varsayılan)
- `0.5` = Yüksek ses

### Farklı ses istiyorum
1. `sound_manager.py` içinde yeni fonksiyon oluşturun
2. Frekans ve süre parametrelerini ayarlayın
3. Import satırını güncelleyin

## Gelecek Geliştirmeler

- [ ] Ses açma/kapama butonu
- [ ] Ses seviyesi ayarı
- [ ] Farklı durumlar için farklı sesler
- [ ] Özel ses dosyası yükleme
- [ ] Sessiz saatler ayarı

## Dosyalar

- `utils/sound_manager.py` - Ses fonksiyonları
- `pages/4_📊_Admin_Dashboard.py` - Bildirim sistemi
- Bu dosya - Döküman

---

**Not**: Web Audio API kullanıldığı için ses dosyasına ihtiyaç yoktur ve internet bağlantısı gerekmez (v1 ve v2 için).
