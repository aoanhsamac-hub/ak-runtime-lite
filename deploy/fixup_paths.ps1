# Fixup: replace D:\AK -> C:\AK in all deploy scripts
$files = Get-ChildItem C:\deploy\*.ps1
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $content = $content -replace 'D:\\AK', 'C:\AK'
    Set-Content -Path $f.FullName -Value $content -NoNewline
    Write-Host "✓ Fixed: $($f.Name)"
}
Write-Host "`nDone. Run .\deploy_all.ps1"
