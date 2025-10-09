# QR Menu AI - Kurulum ve Test Scripti
# PowerShell için hazırlanmıştır

Write-Host "🍕 QR Menu AI - Kurulum Başlatılıyor..." -ForegroundColor Green
Write-Host ""

# 1. Python versiyonunu kontrol et
Write-Host "📌 Python versiyonu kontrol ediliyor..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin." -ForegroundColor Red
    exit 1
}

# 2. Ollama kontrolü
Write-Host ""
Write-Host "📌 Ollama kontrol ediliyor..." -ForegroundColor Yellow
$ollamaCheck = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaCheck) {
    Write-Host "⚠️  Ollama bulunamadı!" -ForegroundColor Red
    Write-Host "Ollama'yı yüklemek için: https://ollama.ai/download" -ForegroundColor Cyan
    $response = Read-Host "Devam etmek istiyor musunuz? (y/n)"
    if ($response -ne 'y') {
        exit 1
    }
} else {
    Write-Host "✅ Ollama kurulu" -ForegroundColor Green
}

# 3. Bağımlılıkları yükle
Write-Host ""
Write-Host "📦 Python paketleri yükleniyor..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Paket yükleme hatası!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Paketler yüklendi" -ForegroundColor Green

# 4. Ollama modellerini kontrol et ve yükle
Write-Host ""
Write-Host "🤖 Ollama modelleri kontrol ediliyor..." -ForegroundColor Yellow

Write-Host "   - llama3.2 modeli kontrol ediliyor..."
$llama32 = ollama list | Select-String "llama3.2"
if (-not $llama32) {
    Write-Host "   📥 llama3.2 indiriliyor (bu biraz zaman alabilir)..."
    ollama pull llama3.2
} else {
    Write-Host "   ✅ llama3.2 mevcut"
}

Write-Host "   - mxbai-embed-large modeli kontrol ediliyor..."
$embed = ollama list | Select-String "mxbai-embed-large"
if (-not $embed) {
    Write-Host "   📥 mxbai-embed-large indiriliyor..."
    ollama pull mxbai-embed-large
} else {
    Write-Host "   ✅ mxbai-embed-large mevcut"
}

# 5. Veritabanını başlat
Write-Host ""
Write-Host "🗄️  Veritabanı oluşturuluyor..." -ForegroundColor Yellow
python database/init_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Veritabanı hatası (zaten var olabilir)" -ForegroundColor Yellow
}

# 6. QR kodları oluştur
Write-Host ""
Write-Host "📱 QR kodları oluşturuluyor..." -ForegroundColor Yellow
python utils/qr_utils.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ QR kodları oluşturuldu" -ForegroundColor Green
}

# 7. Kurulum tamamlandı
Write-Host ""
Write-Host "="*60 -ForegroundColor Green
Write-Host "🎉 Kurulum Tamamlandı!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Uygulamayı başlatmak için:" -ForegroundColor Cyan
Write-Host "   streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 Dokümantasyon için:" -ForegroundColor Cyan
Write-Host "   README.md dosyasını okuyun" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Uygulama şu adreste açılacak:" -ForegroundColor Cyan
Write-Host "   http://localhost:8501" -ForegroundColor White
Write-Host ""

# Uygulamayı başlatma seçeneği
$startApp = Read-Host "Uygulamayı şimdi başlatmak ister misiniz? (y/n)"
if ($startApp -eq 'y') {
    Write-Host ""
    Write-Host "🚀 Uygulama başlatılıyor..." -ForegroundColor Green
    streamlit run app.py
}
