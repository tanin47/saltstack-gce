Write-Host "Started the startup script."

$ErrorActionPreference = "Stop"

$pem = @"
{pem}
"@

$pub = @"
{pub}
"@

$minion_config = @"
master: "{master_ip_address}"
master_finger: "{master_finger}"
id: "{name}"
hash_type: sha256
"@

$username = "tanin"
$password = "TestTest!@#123"
$group = "Administrators"


Write-Host "Started setting admin user."

& NET USER $username $password /add /y /expires:never
& NET LOCALGROUP $group $username /add
& WMIC USERACCOUNT WHERE "Name='$username'" SET PasswordExpires=FALSE

Write-Host "Finished setting up admin user."


Write-Host "Started installing salt-minion."

$url = "https://repo.saltstack.com/windows/Salt-Minion-2016.3.4-AMD64-Setup.exe"
$setup_exe = "c:\salt-setup.exe"

New-Item -ItemType Directory -Path c:\salt\conf\pki\minion -Force
New-Item c:\salt\conf\pki\minion\minion.pem -type file -value $pem
New-Item c:\salt\conf\pki\minion\minion.pub -type file -value $pub

Invoke-WebRequest -Uri $url -OutFile $setup_exe

Start-Process -FilePath $setup_exe -ArgumentList "/S /master={master_ip_address} /minion-name={name} /start-service=0"

New-Item c:\salt\conf\minion -type file -force -value $minion_config

# Sleep for 60 seconds in order to wait for salt-minion to be registered.
Start-Sleep -s 60

Start-Service salt-minion

Write-Host "Finished installing salt-minion."


Write-Host "Finished the startup script."
