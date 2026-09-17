# Path default instalasi Docker Desktop
$DockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Write-Host "Menjalankan Docker Desktop..." -ForegroundColor Green
Start-Process -FilePath $DockerPath

# Menunggu sampai proses Docker Desktop benar-benar berjalan
Do {
    Start-Sleep -Seconds 3
    $DockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
} Until ($DockerProcess)

Write-Host "Docker Desktop berhasil dimuat." -ForegroundColor Cyan