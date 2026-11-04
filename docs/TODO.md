# Breeze Dark Rounded: Roadmap & Task Checklist

- [x] Phase 1: Source Analysis & Decomposition
  - [x] Deep forensic scan of candidate icon packs
  - [x] Catalog sub-designs and isolate alien macOS squircle dumps
  - [x] Document findings in `docs/icon_packs_analysis.md`

- [x] Phase 2: Theme Assembly & Conflict Resolution
  - [x] Extract Chameleon folders with dynamic `ColorScheme-Accent`
  - [x] Extract pure symbolic panels and sidebars
  - [x] Merge rounded KDE application launchers (Breeze Rounded Icons + Breeze_Dark_RC)
  - [x] Resolve visual conflicts (Media controls, Core apps, Folder badges, Action tools)
  - [x] Apply user preference for rounded media playback controls (Option A)

- [x] Phase 3: Plasma 6 System Settings Fix & Diagnostic Audit
  - [x] Fix invalid XDG contexts (`Preferences`, `Apps`) in `index.theme`
  - [x] Purge rogue `preferences-desktop*` squircle files and symlinks from `apps/`
  - [x] Restore official Plasma 6 preferences module icons from `breeze-dark`
  - [x] Restore official Breeze gear/cog to `categories/32/applications-system.svg`
  - [x] Validate zero broken symlinks and zero context warnings in `kf.iconthemes`

- [ ] Phase 4: Repository Standardization & Git Publishing
  - [ ] Move verified build tree to root `Breeze-Dark-Rounded/`
  - [ ] Consolidate verification and maintenance tools in `tools/`
  - [ ] Create `install.sh` and `uninstall.sh` with fish/bash support
  - [ ] Write `README.md` and `AGENTS.md`
  - [ ] Configure GitHub Actions release workflow `.github/workflows/release.yml`
  - [ ] Initialize local git repository with `.gitignore`
  - [ ] Commit with Conventional Commits format
  - [ ] Create private remote GitHub repository `@Segilmez06/breeze-dark-rounded`
  - [ ] Push main branch and tag initial release `v0.1.0`
