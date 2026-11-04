#!/usr/bin/env bash
set -e

ICON_THEME_NAME="Breeze-Dark-Rounded"
DEST_BASE="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
TARGET_DIR="${DEST_BASE}/${ICON_THEME_NAME}"

# Styling
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

if [ -d "${TARGET_DIR}" ]; then
    echo -e "${YELLOW}==> Removing ${TARGET_DIR}...${RESET}"
    rm -rf "${TARGET_DIR}"
    if [ -L "$HOME/.icons/${ICON_THEME_NAME}" ]; then
        rm -f "$HOME/.icons/${ICON_THEME_NAME}"
    fi
    echo -e "${BOLD}${GREEN}✔ Successfully uninstalled ${ICON_THEME_NAME}.${RESET}"
else
    echo -e "Theme is not installed at ${TARGET_DIR}."
fi
