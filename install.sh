#!/bin/bash

trap "echo; exit" INT # terminate with ^C

set -e # exit on first error

echo -e "\nInstalling Eye Care Reminder..."

if [ ! -f ~/bin/eye_care_reminder ]; then
	echo -e "\nNo executable found"
	echo -e "Please download artifact from GitHub Actions & place it at ~/bin/eye_care_reminder"
	exit 1
fi

echo -e "\nGenerating .service file..."

touch eye_care_reminder_service.service

echo -e "\n
[Unit]
Description=Eye Care Reminder Service

[Service]
ExecStart=/home/$USER/bin/eye_care_reminder

Restart=always
RestartSec=60
StartLimitIntervalSec=0

User=$USER
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
" > eye_care_reminder_service.service

echo -e "\n.service file generated!"

cat eye_care_reminder_service.service

echo -e "\nCopying .service file..."

sudo cp eye_care_reminder_service.service /etc/systemd/system/

echo -e "\n.service file copied!"

echo -e "\nEnabling service..."

sudo systemctl daemon-reload
sudo systemctl enable eye_care_reminder_service.service
sudo systemctl start eye_care_reminder_service.service

echo -e "\nService enabled!"

echo -e "\nInstallation completed successfully!!"