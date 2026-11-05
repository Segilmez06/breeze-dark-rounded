# Technical Plan: Breeze Dark Rounded Repository & Release Pipeline

## 1. System Overview & Package Architecture

- **Theme Name**: Breeze Dark Rounded
- **Reverse DNS Identifier**: `net.sarpegilmez.breeze-dark-rounded`
- **Target Desktop**: KDE Plasma 6 on Wayland (Arch Linux / CachyOS)
- **Repository Visibility**: Public (`github.com/Segilmez06/breeze-dark-rounded`)
- **License**: LGPL-3.0-or-later / GPL-3.0-or-later (matching KDE Breeze upstream)

## 2. Directory Layout

```text
breeze-dark-rounded/
├── Breeze-Dark-Rounded/          # Core icon theme directory
│   ├── index.theme               # Validated XDG theme index
│   ├── actions/                  # Symbolic and color action icons
│   ├── animations/               # Spinner and progress animations
│   ├── applets/                  # Plasma widget and panel icons
│   ├── apps/                     # Application launcher icons (Breeze rounded)
│   ├── categories/               # Application category icons
│   ├── devices/                  # Hardware device icons
│   ├── emblems/                  # Status and file emblems
│   ├── emotes/                   # Emoticons
│   ├── mimetypes/                # File type associations
│   ├── places/                   # Chameleon color-tinted folders
│   ├── preferences/              # Plasma 6 System Settings module icons
│   └── status/                   # System tray and notifications
├── docs/                         # Technical documentation
│   ├── PLAN.md                   # This specification file
│   ├── TODO.md                   # Project roadmap and checklist
│   └── icon_packs_analysis.md    # Source forensic analysis
├── tools/                        # Maintenance and verification scripts
│   ├── scan_theme.py             # Complete symlink & index.theme auditor
│   ├── assemble.py               # Theme compilation engine
│   └── generate_rasters.py       # Hi-res PNG rasterizer
├── .github/
│   └── workflows/
│       └── release.yml           # Automated release packaging CI
├── install.sh                    # POSIX & fish compatible local installer
├── uninstall.sh                  # Clean removal script
├── README.md                     # User guide and installation runbook
├── AGENTS.md                     # Master project rules and history
├── LICENSE                       # Licensing terms
└── .gitignore                    # Exclusions for downloads, raw sources, scratch
```

## 3. Automation & Deployment Workflows

1. **Local Installation Script (`install.sh`)**:
   - Detects `$XDG_DATA_HOME` (defaulting to `$HOME/.local/share/icons`).
   - Copies or updates `Breeze-Dark-Rounded` into target directory.
   - Runs `gtk-update-icon-cache -f -t` to rebuild binary cache.
   - Optionally prompts or applies theme directly via `kwriteconfig6`.
2. **One-Liner Execution**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/Segilmez06/breeze-dark-rounded/main/install.sh | bash
   ```
3. **KDE Plasma Native Archive (`.tar.xz`)**:
   - Bundles `Breeze-Dark-Rounded` at root of archive.
   - System Settings $\to$ Icons $\to$ "Install from File..." accepts this `.tar.xz` directly.
4. **GitHub Release CI (`release.yml`)**:
   - Automated via GitHub Actions on tag push `v*`.
   - Packages `Breeze-Dark-Rounded-vX.Y.Z.tar.xz` and generates `SHA256SUMS`.
   - Attaches assets to official GitHub Release.
