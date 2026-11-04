#!/usr/bin/env bash
set -e

# ==============================================================================
# Breeze Dark Rounded - Installer
# Compatible with Linux / KDE Plasma 6 (Wayland & X11)
# ==============================================================================

REPO="Segilmez06/breeze-dark-rounded"
ICON_THEME_NAME="Breeze-Dark-Rounded"
DEST_BASE="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
TARGET_DIR="${DEST_BASE}/${ICON_THEME_NAME}"

# Styling
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}==> Installing Breeze Dark Rounded icon theme...${RESET}"

# Create destination base directory if it doesn't exist
mkdir -p "${DEST_BASE}"

# Check if running from within a cloned repo/local archive
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "${SCRIPT_DIR}" ] && [ -d "${SCRIPT_DIR}/${ICON_THEME_NAME}" ]; then
    echo -e "    Found local theme sources at ${SCRIPT_DIR}/${ICON_THEME_NAME}"
    echo -e "    Syncing files to ${TARGET_DIR}..."
    rm -rf "${TARGET_DIR}"
    cp -r "${SCRIPT_DIR}/${ICON_THEME_NAME}" "${TARGET_DIR}"
else
    # Remote installation: download latest release tarball
    echo -e "    Downloading latest release tarball from GitHub..."
    TAR_URL="https://github.com/${REPO}/releases/latest/download/Breeze-Dark-Rounded.tar.xz"
    TMP_ARCHIVE=$(mktemp /tmp/breeze-dark-rounded-XXXXXX.tar.xz)
    
    if command -v curl >/dev/null 2>&1; then
        curl -sSL -f -o "${TMP_ARCHIVE}" "${TAR_URL}" || {
            echo -e "${YELLOW}    Release asset not yet available or failed to download.${RESET}"
            echo -e "    Falling back to cloning the repository..."
            TMP_DIR=$(mktemp -d /tmp/breeze-dark-rounded-repo-XXXXXX)
            git clone --depth 1 "https://github.com/${REPO}.git" "${TMP_DIR}"
            rm -rf "${TARGET_DIR}"
            cp -r "${TMP_DIR}/${ICON_THEME_NAME}" "${TARGET_DIR}"
            rm -rf "${TMP_DIR}"
        }
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "${TMP_ARCHIVE}" "${TAR_URL}" || {
            echo -e "${YELLOW}    Release asset not yet available or failed to download.${RESET}"
            TMP_DIR=$(mktemp -d /tmp/breeze-dark-rounded-repo-XXXXXX)
            git clone --depth 1 "https://github.com/${REPO}.git" "${TMP_DIR}"
            rm -rf "${TARGET_DIR}"
            cp -r "${TMP_DIR}/${ICON_THEME_NAME}" "${TARGET_DIR}"
            rm -rf "${TMP_DIR}"
        }
    else
        echo -e "${YELLOW}Error: curl or wget is required for remote installation.${RESET}" >&2
        exit 1
    fi

    if [ -f "${TMP_ARCHIVE}" ] && [ -s "${TMP_ARCHIVE}" ]; then
        echo -e "    Extracting into ${DEST_BASE}..."
        rm -rf "${TARGET_DIR}"
        tar -xJf "${TMP_ARCHIVE}" -C "${DEST_BASE}/"
        rm -f "${TMP_ARCHIVE}"
    fi
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    echo -e "    Updating GTK icon cache..."
    gtk-update-icon-cache -f -q -t "${TARGET_DIR}" 2>/dev/null || true
fi

echo -e "\n${BOLD}${GREEN}✔ Breeze Dark Rounded installed successfully to:${RESET}"
echo -e "  ${TARGET_DIR}"

echo -e "\n${BOLD}To activate in KDE Plasma:${RESET}"
echo -e "  1. GUI: Open ${BLUE}System Settings${RESET} → ${BLUE}Colors & Themes${RESET} → ${BLUE}Icons${RESET} → Select ${BOLD}Breeze Dark Rounded${RESET}"
echo -e "  2. CLI: Run ${BLUE}kwriteconfig6 --file kdeglobals --group Icons --key Theme Breeze-Dark-Rounded${RESET}"
