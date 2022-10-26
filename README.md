# Loopbackd
Launch the LoopbackAI daemon and control your computer remotely via Telegram/Whatsapp/SMS


## Installation

```bash
curl -sL https://raw.githubusercontent.com/loopbackai/loopbackd/master/install.sh | sudo bash
loopbackd up
# Follow the instructions to authenticate
```

## Development & Build it from source

Requires python 3.6+ installation in PATH

```bash
# create virtual env and install the dependencies
./dev.sh install

# run in dev mode
./dev.sh run

# build a single binary
./dev.sh build
```

## Building for new architectures / platforms

`"Unsupported system" error on installation`

Install python 3.6+ and clone the project

```bash
./dev.sh build
cp dist/loopbackd* /usr/local/bin/loopbackd
```
Create a systemd service or similar based on the example in ```install.sh```