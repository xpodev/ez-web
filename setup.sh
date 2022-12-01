#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"

NC="\033[0m"

error() {
    echo -e "${RED}ERROR: $1${NC}"
}

warn() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

success() {
    echo -e "${GREEN}$1${NC}"
}

info() {
    echo -e "${BLUE}$1${NC}"
}

if ! command -v pip &> /dev/null
then
    error "pip is not installed. Please install it and try again."
    exit
fi

if ! [ -d .venv ]; then
    info "Creating virtual environment..."
    OUT=$(python3 -m venv .venv)
    if [ $? -ne 0 ]; then
        error "${OUT}\n"
        error "Failed to create virtual environment"
        if [ -d .venv ]; then
            rm -rf .venv
        fi
        exit
    fi
    success "Virtual environment created"
fi


info "Installing dependencies..."
source .venv/bin/activate
PIP_OUT=$(pip install -r reqs.txt)
if [ $? -ne 0 ]; then
    error "${PIP_OUT}\n"
    error "Failed to install dependencies"
    exit
fi

success "Done"

echo -e "
To activate the virtual environment, run:

    ${YELLOW}source${NC} .venv/bin/activate


You can now run the app with:

    ${YELLOW}python3${NC} src/main.py


or watch for changes with:

    ${YELLOW}watchfiles${NC} \"python3 src/main.py\" src

"
info "Happy coding!
"
