# Breeze Dark Rounded

Breeze Dark Rounded is a clean icon theme for KDE Plasma 6. It combines softly rounded folders with dynamic accent tinting, pure monochrome symbolic icons for panels and sidebars, and rounded application icons. It removes third-party squircle and badge modifications to maintain visual consistency with vanilla Breeze.

---

## Features

- **Softly Rounded Geometry**: Folders, core application icons, and media controls have smooth rounded corners.
- **Dynamic Accent Color Tinting**: Folders dynamically inherit your active KDE Plasma accent color via `ColorScheme-Accent`.
- **Pure Symbolic Panels**: Panel and sidebar icons use clean monochrome vectors (`ColorScheme-Text` / `currentColor`).
- **Aesthetic Purity**: Zero macOS-style squircles, circular badges, or iOS dumps. Missing icons fall back to upstream Breeze and vendor `hicolor`.
- **Plasma 6 Certified**: All System Settings sidebar modules resolve to dedicated native SVGs without fallback regressions.
- **High-DPI Ready**: Includes complete `@2x` and `@3x` scaled directory trees and hi-res raster caches for 4K and multi-monitor displays.

---

## Installation

### Method 1: Single-Command Quick Install (Recommended)

Run this command in your terminal (`bash` or `fish`):

```bash
curl -sSL https://raw.githubusercontent.com/Segilmez06/breeze-dark-rounded/main/install.sh | bash
```

### Method 2: Download Release Archive (Offline / One-Liner)

Download and extract the latest release archive directly into your user icon directory:

```bash
mkdir -p ~/.local/share/icons && curl -sSL https://github.com/Segilmez06/breeze-dark-rounded/releases/latest/download/Breeze-Dark-Rounded.tar.xz | tar -xJ -C ~/.local/share/icons/
```

### Method 3: KDE Plasma GUI ("Install from File...")

1. Go to the [Releases](https://github.com/Segilmez06/breeze-dark-rounded/releases/latest) page.
2. Download `Breeze-Dark-Rounded.tar.xz`.
3. Open **System Settings** → **Colors & Themes** → **Icons**.
4. Click **Install from File...** at the bottom.
5. Select the downloaded `Breeze-Dark-Rounded.tar.xz` file.
6. Select **Breeze Dark Rounded** from the icon list and click **Apply**.

---

## Activation

To apply the theme immediately from the command line:

```bash
kwriteconfig6 --file kdeglobals --group Icons --key Theme Breeze-Dark-Rounded
```

To update the icon cache manually:

```bash
gtk-update-icon-cache -f -t ~/.local/share/icons/Breeze-Dark-Rounded
```

---

## Removal

To remove the theme, run:

```bash
rm -rf ~/.local/share/icons/Breeze-Dark-Rounded
```

Or execute the provided uninstaller:

```bash
./uninstall.sh
```

---

## Validation & Quality Assurance

This repository includes an automated verification script to audit all symlinks, contexts, and directory declarations:

```bash
python3 tools/scan_theme.py
```

Current test status:
- Total entries: `30,700`
- Broken symlinks: `0`
- Invalid XDG contexts: `0`
- High-DPI scaled directories: `110`

---

## License

This project is licensed under the GNU Lesser General Public License Version 3 (LGPL-3.0-or-later) and GNU General Public License Version 3 (GPL-3.0-or-later) to match upstream KDE Breeze. See [LICENSE](LICENSE) for details.
