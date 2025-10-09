# 📱 Mobil Test Kılavuzu - QR Menu Restaurant

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum (ÖNERİLEN)

PowerShell'de çalıştırın:

```powershell
.\mobile_test.ps1
```

Bu script otomatik olarak:
- ✅ IP adresinizi bulur
- ✅ QR kod oluşturur
- ✅ URL'yi panoya kopyalar
- ✅ Streamlit'i mobil erişim için başlatır

---

## 📋 Manuel Kurulum

### 1. IP Adresinizi Bulun

```powershell
ipconfig
```

`IPv4 Address` satırındaki adresi not edin (örn: `192.168.1.10`)

### 2. Streamlit'i Ağa Açık Başlatın

```powershell
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 3. Mobil Cihazda Açın

iPhone/Android Safari/Chrome'da:
```
http://[IP_ADRESİNİZ]:8501
```

**Örnek:** `http://192.168.1.10:8501`

---

## ✅ Kontrol Listesi

- [ ] Her iki cihaz da **aynı WiFi ağında**
- [ ] Streamlit `0.0.0.0` adresinde çalışıyor
- [ ] Windows Firewall port 8501'e izin veriyor
- [ ] Mobil cihaz mobil veri değil WiFi kullanıyor

---

## 🔥 Sorun Giderme

### Problem: "Siteye ulaşılamıyor"

**Çözüm 1: Firewall Kontrolü**
```powershell
# Windows Defender Firewall'da yeni kural ekleyin
New-NetFirewallRule -DisplayName "Streamlit Mobile" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow
```

**Çözüm 2: IP Adresini Doğrulayın**
```powershell
# Aktif ağ bağlantınızın IP'sini göster
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"} | Select-Object IPAddress, InterfaceAlias
```

**Çözüm 3: Ping Testi**

Mobil cihazınızda bir terminal uygulaması kullanarak:
```bash
ping [IP_ADRESİNİZ]
```

Yanıt alıyorsanız ağ bağlantısı var demektir.

---

### Problem: "Connection Refused"

Streamlit'in doğru şekilde başladığından emin olun:
```powershell
# Process kontrolü
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"}

# Port kontrolü
Get-NetTCPConnection -LocalPort 8501
```

---

### Problem: QR Kod Oluşturulamıyor

QR kod modülünü yükleyin:
```powershell
pip install qrcode[pil]
```

Tekrar deneyin:
```powershell
.\mobile_test.ps1
```

---

## 🌐 Alternatif: Ngrok ile Genel Erişim

Farklı ağlardan (ofis, ev, mobil veri) test etmek için:

### 1. Ngrok İndirin
https://ngrok.com/download

### 2. Streamlit'i Başlatın
```powershell
streamlit run app.py
```

### 3. Başka Bir Terminal'de Ngrok'u Çalıştırın
```powershell
ngrok http 8501
```

### 4. Ngrok URL'sini Kullanın

Ngrok size şöyle bir URL verir:
```
https://xxxx-xx-xx-xxx-xxx.ngrok-free.app
```

Bu URL'yi **herhangi bir cihazda, herhangi bir ağda** açabilirsiniz! 🌍

---

## 📊 Test Checklist

Mobil cihazda şunları test edin:

### Müşteri Tarafı
- [ ] 🏠 Ana sayfa yükleniyor
- [ ] 🍽️ Menü sayfası çalışıyor
- [ ] 🛒 Sepete ürün eklenebiliyor
- [ ] 💬 AI Asistan yanıt veriyor
- [ ] 📱 Sidebar navigasyon çalışıyor

### Admin Tarafı
- [ ] 🔐 Admin login çalışıyor
- [ ] 📊 Dashboard yükleniyor
- [ ] 🏓 Masa yönetimi çalışıyor
- [ ] 🍽️ Menü yönetimi çalışıyor
- [ ] 📈 Raporlar görüntüleniyor

---

## 💡 İpuçları

1. **Safari Private Mode**: Bazı durumlarda gizli mod daha iyi çalışır
2. **Cache Temizleme**: Sorun yaşarsanız tarayıcı cache'ini temizleyin
3. **HTTPS Uyarısı**: Ngrok kullanıyorsanız, güvenlik uyarısını "Advanced -> Proceed" ile geçin
4. **Port Değiştirme**: 8501 yerine farklı port (örn: 8502) deneyin
5. **Antivirus**: Geçici olarak antivirüs yazılımınızı devre dışı bırakın

---

## 🎯 Hızlı Komutlar

```powershell
# Test script'ini çalıştır (tüm adımları otomatik yapar)
.\mobile_test.ps1

# IP adresini göster
ipconfig | Select-String "IPv4"

# Streamlit'i mobil erişim için başlat
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

# Firewall kuralı ekle
New-NetFirewallRule -DisplayName "Streamlit" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow

# Ngrok ile genel erişim
ngrok http 8501
```

---

## 📞 Destek

Sorun yaşıyorsanız şunları kontrol edin:

1. **Ağ Bağlantısı**: İki cihaz da aynı WiFi'de mi?
2. **Firewall**: Windows Defender port 8501'e izin veriyor mu?
3. **Streamlit Çalışıyor mu**: `http://localhost:8501` bilgisayarda açılıyor mu?
4. **Doğru IP**: IP adresini doğru mu girdiniz?

---

## 🎉 Başarılı Test

Her şey çalışıyorsa:
- ✅ Mobil cihazdan menü görüntüleniyor
- ✅ Ürünler sepete eklenebiliyor
- ✅ AI asistan sorulara yanıt veriyor
- ✅ Admin paneline giriş yapılabiliyor

**Tebrikler! QR Menu Restaurant mobil uyumlu! 🚀📱**

---

## 📚 Ek Kaynaklar

- Streamlit Deployment Docs: https://docs.streamlit.io/deploy
- Ngrok Documentation: https://ngrok.com/docs
- Network Troubleshooting: https://learn.microsoft.com/en-us/windows-server/networking/

---

**Son Güncelleme**: 7 Ekim 2025
**Versiyon**: QR Menu AI v2.0
