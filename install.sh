#!/bin/bash

# Download binary

if [[ $(uname -s) == "Linux" ]] && [[ $(arch) == "x86_64" ]]; then
    curl -o /usr/local/bin/loopbackd https://github.com/loopbackai/loopbackd/releases/latest/download/loopbackd_Linux_x86_64
else
    echo "Unsupported system."
    exit 1
fi

# Create Systemd service

cat <<EOM >"/etc/systemd/system/loopbackd.service"
[Unit]
Description=Loopbackd service to connect remotely to your machine, loopbackd --help for more info
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
RemainAfterExit=yes
User=$USER
ExecStart=/usr/local/bin/loopbackd daemon
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOM

systemctl start loopbackd
systemctl enable loopbackd