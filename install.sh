#!/bin/bash

# Download binary

OS=$(uname -s)
ARCH=$(arch)

# stop & disable service if exists
{
    systemctl stop loopbackd
    systemctl disable loopbackd
} &> /dev/null

curl -sfLo /usr/local/bin/loopbackd https://github.com/loopbackai/loopbackd/releases/latest/download/loopbackd_"$OS"_"$ARCH"
CURL_RESPONSE=$?

if [[ $CURL_RESPONSE == 0 ]]
then
    chmod +x /usr/local/bin/loopbackd
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
RestartSec=5
TimeoutStartSec=0
User=$SUDO_USER
ExecStart=/usr/local/bin/loopbackd daemon

[Install]
WantedBy=multi-user.target
EOM

systemctl start loopbackd
systemctl enable loopbackd

echo "Installed successfully - run 'loopbackd up' for the next step"