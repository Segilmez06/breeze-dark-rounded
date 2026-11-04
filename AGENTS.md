# AGENTS.md — Breeze Dark Rounded

## Project Architecture & Overview
Breeze Dark Rounded (`net.sarpegilmez.breeze-dark-rounded`) is a unified, curated KDE Plasma 6 icon theme that combines softly rounded folders with dynamic accent tinting, pure monochrome symbolics for panels and sidebars, and clean rounded native KDE application icons. It strictly purges all foreign macOS/iOS squircles and Android badges, ensuring complete aesthetic purity with vanilla Breeze fallback.

### Environment & Tooling
- **Target OS**: Linux (CachyOS / Arch Linux)
- **Desktop Environment**: KDE Plasma 6 on Wayland (`kwin_wayland`)
- **Default User Shell**: `fish` (scripts provide POSIX/bash/fish compatibility)
- **Theme Destination**: `~/.local/share/icons/Breeze-Dark-Rounded/`
- **Cache Management**: `gtk-update-icon-cache -f -t ~/.local/share/icons/Breeze-Dark-Rounded/`
- **Validation**: `python3 tools/scan_theme.py`

### Key Architectural Decisions
1. **Dynamic Folder Tinting**:
   - Folders (`places/32-96`) utilize `class="ColorScheme-Accent"` with `id="current-color-scheme"` and `fill:currentColor`. This enables native KDE Plasma 6 accent color tinting across all folder variants.
2. **Pure Symbolics**:
   - Sidebar and panel icons (`actions/`, `status/`, `places/` 16px/22px/24px) are strictly monochrome, color-adaptive vectors (`currentColor` / `ColorScheme-Text`).
3. **Plasma 6 System Settings Compliance**:
   - Directory definitions in `index.theme` for `preferences/*` MUST use `Context=Applications` and `Type=Scalable` (`MinSize=32`, `MaxSize=256`). `Context=Preferences` is invalid in KDE Frameworks (`KIconThemes`) and causes directory rejection.
   - Suffix-stripping fallback requires `apps/48` to exclude generic settings icons (`preferences-desktop.svg`), ensuring queries resolve to dedicated modules in `preferences/32`.
4. **Media Controls**:
   - Standardized on Option A: rounded circular borders with curved inner playback glyphs across all sizes (16, 22, 24, 32) and symbolic counterparts.
5. **Alien Squircle Prohibition**:
   - Purged 3,200+ WhiteSur/BigSur third-party squircle app dumps. Un-themed applications fall back cleanly to vanilla Breeze or their vendor branding (`hicolor`).

### Module Map
- `Breeze-Dark-Rounded/`: The active icon theme tree ready for installation.
- `docs/`: Technical planning (`PLAN.md`), roadmap (`TODO.md`), and source forensic analysis (`icon_packs_analysis.md`).
- `tools/`: Python verification and maintenance utilities (`scan_theme.py`).
- `.github/workflows/`: Automated GitHub Actions release pipeline (`release.yml`).
- `install.sh` / `uninstall.sh`: One-liner installer and clean removal scripts.

### Progress & Changelog
- **2026-11-04**: Forensic analysis of 5 source packages; identified 5 sub-designs and isolated macOS squircle pollution.
- **2026-11-05**: Generated multi-page visual conflict selector; applied user preferences for KDE apps, folder badges, and actions.
- **2026-11-05**: Diagnosed and resolved Plasma 6 System Settings squircle fallback regression by fixing invalid XDG contexts, restoring official preferences SVGs, and purging rogue `apps/` overrides.
- **2026-11-05**: Completed 30,622-entry scan with zero broken links; converted absolute symlinks to relative; added `@2x`/`@3x` High-DPI scaled symlinks.
- **2026-11-05**: Switched media controls to Option A (rounded circular border & curved glyphs); created release pipeline, documentation, and installation scripts.
