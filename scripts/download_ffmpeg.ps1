# FFmpeg Download Script
Write-Host "Downloading FFmpeg..." -ForegroundColor Green

$toolsDir = ".\tools"
$ffmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
$ffmpegZip = "$toolsDir\ffmpeg.zip"

try {
    Write-Host "Downloading FFmpeg..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $ffmpegZip -UseBasicParsing
    
    Write-Host "Extracting..." -ForegroundColor Yellow
    Expand-Archive -Path $ffmpegZip -DestinationPath $toolsDir -Force
    
    Write-Host "FFmpeg download completed!" -ForegroundColor Green
    Write-Host "Location: $toolsDir" -ForegroundColor Cyan
    
    # Cleanup
    Remove-Item $ffmpegZip
    
} catch {
    Write-Host "Download failed: $($_.Exception.Message)" -ForegroundColor Red
}