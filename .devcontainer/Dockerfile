# Start from the universal Codespaces base image
FROM mcr.microsoft.com/vscode/devcontainers/universal:2-focal

# Install additional OS packages
RUN apt-get update && apt-get -y install --no-install-recommends \
    python3.8-venv \
    gcc

ARG USER="codespace"
ARG VENV_PATH="/home/${USER}/venv"
ENV PYTHONUSERBASE=${VENV_PATH}

# Copy requirements and makefile to set up environment
COPY requirements.txt /requirements.txt
COPY Makefile /Makefile

# Set up Python virtual environment and install dependencies
RUN su $USER -c "/usr/bin/python3 -m venv ${VENV_PATH}" \
    && su $USER -c "${VENV_PATH}/bin/pip install -r /requirements.txt" \
    && rm -rf /requirements.txt
