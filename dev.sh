#!/bin/bash

while [[ $# -gt 0 ]]; do
  case $1 in
  install)
    python -m venv venv
    ./venv/bin/pip install -r requirements.txt
    exit 0
    ;;
  build)
    rm -rf venv_build
    python -m venv venv_build
    ./venv_build/bin/pip install -r requirements.txt
    ./venv_build/bin/pyinstaller main.py --onefile
    mv dist/main dist/loopbackd_$(uname)_$(arch)
    rm -rf venv_build
    exit 0
    ;;
  run)
    shift
    ./venv/bin/python main.py $@
    exit 0
    ;;
  -* | --*)
    echo "Unknown option $1"
    exit 1
    ;;
  *)
    POSITIONAL_ARGS+=("$1") # save positional arg
    shift                   # past argument
    ;;
  esac
done

echo "Doing nothing"