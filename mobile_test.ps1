# Mobile Test Script - QR Menu Restaurant
# Simple version for mobile access configuration

Write-Host "Mobile Test - QR Menu Restaurant" -ForegroundColor Cyan
Write-Host ""

# Get local IP address
Write-Host "Finding IP address..." -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.InterfaceAlias -notlike "*Loopback*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object -First 1).IPAddress

if (-not $ipAddress) {
    Write-Host "ERROR: Could not find IP address!" -ForegroundColor Red
    Write-Host "Please check your WiFi/Ethernet connection." -ForegroundColor Yellow
    exit 1
}

$port = "8501"
$localUrl = "http://$ipAddress`:$port"

Write-Host "SUCCESS: IP Address found: $ipAddress" -ForegroundColor Green
Write-Host "Mobile URL: $localUrl" -ForegroundColor Green
Write-Host ""

# Generate QR code
Write-Host "Generating QR code for mobile access..." -ForegroundColor Yellow

$qrPython = @"
import qrcode
url = '$localUrl'
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save('static/qr_codes/mobile_access.png')
qr_ascii = qrcode.QRCode()
qr_ascii.add_data(url)
qr_ascii.make()
qr_ascii.print_ascii()
print('\nQR code saved: static/qr_codes/mobile_access.png')
"@

try {
    $qrPython | Out-File -FilePath "temp_qr.py" -Encoding UTF8
    python temp_qr.py
    Remove-Item "temp_qr.py" -ErrorAction SilentlyContinue
} catch {
    Write-Host "WARNING: Could not generate QR code (qrcode module may be missing)" -ForegroundColor Yellow
    Write-Host "Install with: pip install qrcode[pil]" -ForegroundColor Gray
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "MOBILE ACCESS INFORMATION" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Browser URL:" -ForegroundColor White
Write-Host "  $localUrl" -ForegroundColor Green
Write-Host ""
Write-Host "  For iPhone/Android:" -ForegroundColor White
Write-Host "  1. Connect to the SAME WiFi network" -ForegroundColor Yellow
Write-Host "  2. Open Safari/Chrome and enter the URL above" -ForegroundColor Yellow
Write-Host "  3. Or scan QR code: static/qr_codes/mobile_access.png" -ForegroundColor Yellow
Write-Host ""
Write-Host "  IMPORTANT:" -ForegroundColor White
Write-Host "  - Both devices must be on the SAME WiFi network!" -ForegroundColor Magenta
Write-Host "  - Firewall may block port 8501" -ForegroundColor Magenta
Write-Host "  - If not working: Allow port 8501 in Windows Defender Firewall" -ForegroundColor Magenta
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Copy URL to clipboard
Set-Clipboard -Value $localUrl
Write-Host "URL copied to clipboard!" -ForegroundColor Green
Write-Host ""

# Ask to start Streamlit
Write-Host "Start Streamlit now? (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y' -or $response -eq '') {
    Write-Host ""
    Write-Host "Starting Streamlit..." -ForegroundColor Green
    Write-Host "  - Server binding to: 0.0.0.0:$port (all network interfaces)" -ForegroundColor Gray
    Write-Host "  - Your access URL: $localUrl" -ForegroundColor Cyan
    Write-Host "  - Press CTRL+C to stop" -ForegroundColor Gray
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "IMPORTANT: Use $localUrl on your mobile device!" -ForegroundColor Yellow
    Write-Host "           (NOT http://0.0.0.0:8501 - that won't work!)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Start Streamlit with network access
    streamlit run app.py --server.address 0.0.0.0 --server.port $port
} else {
    Write-Host ""
    Write-Host "Streamlit not started." -ForegroundColor Yellow
    Write-Host "To start manually, run:" -ForegroundColor White
    Write-Host "streamlit run app.py --server.address 0.0.0.0 --server.port $port" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then access from mobile: $localUrl" -ForegroundColor Green
    Write-Host ""
}
