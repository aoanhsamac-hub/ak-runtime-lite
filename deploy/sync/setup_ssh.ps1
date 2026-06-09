$ErrorActionPreference = "Stop"
$logFile = "D:\AK\logs\setup_ssh.log"
$keyPath = "$env:USERPROFILE\.ssh\ak_vps"
$configPath = "$env:USERPROFILE\.ssh\config"
$vpsHost = "100.81.12.50"
$vpsUser = "GiangKhoi"

Write-Host "=== AK-AUTO-RUNTIME-SYNC-01 :: SSH Setup ===" -ForegroundColor Cyan

# Step 1: Create .ssh directory if not exists
$sshDir = Split-Path -Parent $keyPath
if (-not (Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }

# Step 2: Generate SSH key if not exists
if (-not (Test-Path "$keyPath")) {
    Write-Host "[1/4] Tao SSH key..." -ForegroundColor Yellow
    ssh-keygen -t ed25519 -f $keyPath -N "" -q
    Write-Host "  -> Da tao: $keyPath" -ForegroundColor Green
} else {
    Write-Host "[1/4] SSH key da ton tai: $keyPath" -ForegroundColor Green
}

# Step 3: Create SSH config
$configContent = @"

Host ak-vps
    HostName $vpsHost
    User $vpsUser
    IdentityFile $keyPath
    StrictHostKeyChecking no
    UserKnownHostsFile NUL

"@
$existingConfig = ""
if (Test-Path $configPath) { $existingConfig = Get-Content $configPath -Raw }
if ($existingConfig -notmatch "Host ak-vps") {
    Write-Host "[2/4] Tao SSH config..." -ForegroundColor Yellow
    Add-Content -Path $configPath -Value $configContent -Encoding UTF8
    Write-Host "  -> Da them host 'ak-vps' vao config" -ForegroundColor Green
} else {
    Write-Host "[2/4] SSH config da co host ak-vps" -ForegroundColor Green
}

# Step 4: Copy public key to VPS
Write-Host "[3/4] Copy public key len VPS..." -ForegroundColor Yellow
Write-Host "  -> VPS: $vpsUser@$vpsHost"
Write-Host "  -> Can nhap PASSWORD cua VPS lan cuoi cung!" -ForegroundColor Red
$pubKey = Get-Content "$keyPath.pub" -Raw
ssh $vpsUser@$vpsHost "mkdir -p .ssh 2>nul & echo $pubKey >> .ssh\authorized_keys & type nul >> .ssh\authorized_keys" 2>&1 | Out-Host
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Copy public key thanh cong!" -ForegroundColor Green
} else {
    Write-Host "  -> LOI: Khong copy duoc public key. Thu lai bang tay." -ForegroundColor Red
    Write-Host "  -> Lenh: type `"$keyPath.pub`" | ssh $vpsUser@$vpsHost `"mkdir -p .ssh 2>nul & cat >> .ssh\authorized_keys`""
    exit 1
}

# Step 5: Test connection
Write-Host "[4/4] Kiem tra SSH khong password..." -ForegroundColor Yellow
$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>&1
if ($test -eq "OK") {
    Write-Host "  -> THANH CONG! SSH vao VPS khong can password." -ForegroundColor Green
    "SSH_SETUP_OK" | Out-File -FilePath "D:\AK\logs\.ssh_done" -Encoding UTF8
} else {
    Write-Host "  -> THAT BAI. Van can password. Kiem tra lai authorized_keys tren VPS." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== HOAN TAT SSH SETUP ===" -ForegroundColor Cyan
