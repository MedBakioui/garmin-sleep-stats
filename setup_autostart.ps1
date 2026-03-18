$Action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c "e:\@Sleep\launch_sleep_app.bat"'
$Trigger = New-ScheduledTaskTrigger -Daily -At 5am
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -TaskName "GarminSleepStatsAutoStart" -Description "Lancement automatique de l'application Garmin Sleep Stats à 5h du matin." -Force
