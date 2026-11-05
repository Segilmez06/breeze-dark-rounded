# KDE Breeze Icon Themes Analysis & Frankenstein Architecture Plan

## 1. Executive Summary & Core Objective

The goal is to create a clean, consistent, unified **KDE Plasma icon theme** that fulfills four core design requirements:
1. **Rounded system geometry**: Softly rounded folders and native KDE app icons without harsh 90° edges.
2. **Pure symbolic panels and sidebars**: Monochrome, color-adaptive icons (`currentColor` / `ColorScheme-Text`) for Plasma panels, system trays, and Dolphin sidebars.
3. **Colored launcher and app icons**: Native, high-contrast colored icons for applications and launcher menus—strictly adhering to KDE's visual identity.
4. **Artistic purity (Zero macOS / Windows pollution)**: Eliminating all Apple-style squircles (continuous-curvature drop-shadow rounded squares), iOS-style badges, and Android circles. Un-themed applications will cleanly fall back to vanilla Breeze or their official upstream branding (`hicolor`).

---

## 2. Inventory & Forensic Analysis of Available Packages

| Package | Location | Regular SVGs | Symlinks | Broken Symlinks | Total Files | FollowsColorScheme | macOS / Alien Squircle Pollution |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Upstream Round Chameleon** | `downloads/...1608771.tar.xz` | 9,372 | 15,087 | 0 | 24,459 | Yes (`ColorScheme-Highlight`) | **Severe** (3,273+ third-party squircle/circle apps in `apps/48`) |
| **Breeze Chameleon Dark** | `sources/Breeze Chameleon Dark` | 10,119 | 15,642 | 2 | 25,761 | Yes | **Severe** (3,444+ third-party apps in `apps/48`) |
| **Fixed (User's Cleanup)** | `sources/Breeze-Round-Chameleon...Fixed` | 6,281 | 14,732 | **3,371** | 21,013 | Yes | **Moderate** (1,695 apps left in `apps/48`, 1,644 broken symlinks) |
| **Breeze Rounded Icons** | `sources/Breeze Rounded Icons` | 7,345 | 1,056 | 10 | 8,401 | Yes | **Minimal / None** (291 apps in `apps/48`, pure KDE core set) |
| **Breeze Dark RC (ju1464)** | `sources/Breeze_Dark_RC` | 1,213 | 4,535 | 0 | 5,748 | No (Static Breeze blue `#3daee9`) | **None** (86 regular Breeze apps in `apps/48`, 529 symlinks) |
| **Vanilla Breeze Dark** | `/usr/share/icons/breeze-dark` | 4,778 | 15,550 | 0 | 20,328 | System reference | **None** (331 official KDE apps in `apps/48`) |

---

## 3. Decomposition: The 5 Sub-Designs in the Spaghetti

The upstream theme `Breeze-Round-Chameleon Dark Icons` is not a single coherent creation—it is a collage of five distinct layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UPSTREAM "ROUND CHAMELEON" SPAGHETTI                 │
│                                                                        │
│  ┌───────────────────────────┐       ┌──────────────────────────────┐  │
│  │ Layer 1: Chameleon Folders│       │ Layer 2: Chameleon Symbolics │  │
│  │ Dynamic ColorScheme-High- │       │ Actions/Status/Places 16-24  │  │
│  │ light (Plasma accent tint)│       │ currentColor & Text scheme   │  │
│  └─────────────┬─────────────┘       └──────────────┬───────────────┘  │
│                │                                    │                  │
│  ┌─────────────┴─────────────┐       ┌──────────────┴───────────────┐  │
│  │ Layer 3: Rounded KDE Apps │       │ Layer 4: macOS/Alien Squircle│  │
│  │ ~200-300 core KDE apps    │       │ 3,200+ WhiteSur/BigSur/iOS   │  │
│  │ softly rounded corners    │       │ third-party app icon dump    │  │
│  └───────────────────────────┘       └──────────────┬───────────────┘  │
│                                                     │                  │
│  ┌──────────────────────────────────────────────────┴───────────────┐  │
│  │ Layer 5: Non-standard foreign layouts (16x16, 22x22, 8x8 emblems)│  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### Sub-Design 1: Chameleon Dynamic Folders (Keep)
* **Origins**: Created by `l4k1` (KDE Store author).
* **Characteristics**: In `places/32`, `places/48`, `places/64`, `places/96`, the folder SVGs use inline CSS:
  ```xml
  <style type="text/css" id="current-color-scheme">
    .ColorScheme-Highlight { color: #3daee9; }
  </style>
  <path style="fill:currentColor;fill-opacity:1;..." ... />
  ```
* **Why it works**: Folders automatically adapt when you switch your KDE Plasma accent color in System Settings (e.g. emerald, purple, orange, sapphire).
* **Geometry**: Moderately rounded corners on the tabs and bottom folder body.

### Sub-Design 2: Chameleon Monochrome Symbolics (Keep & Patch)
* **Origins**: Sourced from Breeze monochrome action sets, injected with `ColorScheme-Text` inline stylesheets.
* **Characteristics**: Used in `places/16`, `places/22`, `places/24`, `actions/16`, `actions/22`, `actions/24`, and `status/16`, `status/22`, `status/24`.
* **Why it works**: Renders sharp 1px-aligned symbolic glyphs inside the Dolphin sidebar, Plasma system tray, and toolbars, adjusting automatically to dark or light text.
* **The Flaw (Size Gaps)**:
  - **704 icons** present in `actions/22` are completely missing in `actions/16`.
  - **3,296 icons** present in `actions/22` are missing in `actions/32`.
  - **496 icons** in `status/22` are missing in `status/16`.
  - Dedicated `symbolic/` directory (used by GTK/GNOME apps like Firefox, Lutris, GIMP) was removed or omitted from upstream `Round Chameleon` (though present in `Breeze Chameleon Dark`).

### Sub-Design 3: Native KDE Breeze App Icons with Rounded Corners (Keep)
* **Origins**: Found in `Breeze Rounded Icons` (198 regular SVGs) and `Breeze_Dark_RC` by Jorge Cabrera / ju1464 (86 regular SVGs).
* **Characteristics**: Classic Breeze metaphors (folded page corners, isometric tools, KDE gears) where sharp outer corners have been converted to continuous rounded bevels without encasing them inside a squircle box.
* **Examples**: `dolphin`, `kate`, `kcalc`, `ark`, `okular`, `systemsettings`, `konversation`, `gwenview`, `kdenlive`.

### Sub-Design 4: macOS / WhiteSur / Big Sur Squircle Dump (PURGE)
* **Origins**: Mass-imported from macOS-clone Linux icon packs (WhiteSur, Big Sur, Cupertino, McMojave) to inflate the icon count to 3,500+.
* **Characteristics**: 
  - 48x48 SVGs featuring a continuous-curvature Apple squircle background with radial dropshadows and tiny centered logos.
  - White circular buttons with thick borders.
  - Radical clash with Breeze's visual grammar (flat/diagonal lighting vs Apple skeuomorphic glass gradients).
* **In Fixed attempt**: 1,869 files were removed, but 1,695 remained, leaving over 1,600 broken symlinks behind.

### Sub-Design 5: Orphaned XDG Directory Artifacts (PURGE)
* Directories named `16x16/emblems`, `22x22/emblems`, `8x8/emblems` at the root level.
* These violate KDE Breeze conventions (`emblems/16`, `emblems/22`, `emblems/8`) and were never declared in `index.theme`.

---

## 4. Why the Previous "Fixed" Effort Broke

When cleaning up `Breeze-Round-Chameleon Dark Icons Fixed`:
1. **3,371 Broken Symlinks**: Deleting targets in `apps/48` and `mimetypes/` left all corresponding aliases dangling:
   - `apps/48`: 1,644 broken symlinks (e.g. `org.mozilla.firefox.svg -> firefox.svg` when `firefox.svg` was deleted).
   - `mimetypes/64`: 786 broken symlinks.
   - `mimetypes/32`: 423 broken symlinks.
2. **Missing App Fallbacks**: Deleting standard app names without providing alternative symlinks or ensuring a fallback hierarchy caused launchers to fall back inconsistently.
3. **Symbolic Size Gaps Remained**: Plasma panels set to 24px, 32px, or 48px thickness encountered missing icons and fell back to inconsistent upstream shapes.

---

## 5. The "Frankenstein" Architecture Specification

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE FRANKENSTEIN BREEZE THEME                     │
│                                                                        │
│  [Inherits = breeze-dark, breeze, hicolor]                             │
│                                                                        │
│  1. PLACES (Folders)                                                   │
│     • 32, 48, 64, 96: Chameleon Rounded (l4k1) [Dynamic Color Tint]    │
│     • 16, 22, 24: Symbolic Monochrome (Dolphin sidebar)                │
│                                                                        │
│  2. ACTIONS, STATUS, DEVICES, PREFERENCES                              │
│     • Base: Chameleon Monochrome Symbolics                             │
│     • Size Gap Bridging: Complete 16, 22, 24, 32 matrix via symlinks   │
│     • GTK Compatibility: Scalable symbolic/ directories registered      │
│                                                                        │
│  3. APPLICATIONS (apps/)                                               │
│     • Core KDE Apps: Merged Rounded Set (BRI 198 + Breeze_Dark_RC 86)  │
│     • macOS / Squircle Dump: 100% PURGED                               │
│     • Clean Symlinks: Zero broken symlinks                             │
│     • Missing Apps: Fall back to vanilla Breeze or official hicolor    │
│                                                                        │
│  4. MIMETYPES & APPLETS                                                │
│     • Rounded Chameleon mimetypes & applets                            │
│     • Orphaned/broken symlinks cleaned                                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Component Sourcing Matrix

| Component | Source Package | Action |
| :--- | :--- | :--- |
| **Chameleon Folders** (`places/32-96`) | `Breeze-Round-Chameleon Dark Icons` | Extract directly; retain `ColorScheme-Highlight`. |
| **Sidebar Places** (`places/16-24`) | `Breeze-Round-Chameleon Dark Icons` | Extract directly; ensure complete 16/22/24 coverage. |
| **Core Rounded KDE Apps** (`apps/48`, `32`) | `Breeze Rounded Icons` + `Breeze_Dark_RC` | Merge the 198 apps from BRI and the 86 apps from RC. |
| **Symbolic Actions & Status** (`actions/`, `status/`) | `Breeze-Round-Chameleon` + `Breeze Chameleon Dark` | Use Chameleon symbolics; synthesize missing 16px/24px/32px sizes. |
| **GTK Symbolic Folders** (`*/symbolic`) | `Breeze Chameleon Dark` | Include `actions/symbolic`, `places/symbolic`, `status/symbolic`, `devices/symbolic`. |
| **Alien macOS / Squircles** | Any | **Exclude completely**. |
| **Foreign Directories** (`16x16`, `22x22`, `8x8`) | Any | **Exclude completely**. |
| **Missing Gaps** | `breeze-dark` / `hicolor` | Handled via `Inherits=breeze-dark,breeze,hicolor`. |

---

## 6. Execution Plan & Next Steps

1. **Workspace Assembly Directory**: Create a clean output staging area: `build/Breeze-Round-Chameleon-Dark-Frankenstein`.
2. **Selective Component Extraction**:
   - Copy Chameleon `places` (16, 22, 24, 32, 48, 64, 96).
   - Copy Chameleon `actions`, `status`, `devices`, `preferences`, `applets`, `emblems`, `mimetypes`.
   - Copy dedicated `*/symbolic` trees from `Breeze Chameleon Dark`.
   - Copy ONLY genuine rounded KDE apps from `Breeze Rounded Icons` and `Breeze_Dark_RC`.
3. **Symbolic Gap Synthesis**:
   - Run a link-generation script to bridge missing sizes (if an icon exists in 22px but is absent in 16px or 24px, create a normalized symlink).
4. **Symlink Pruning & Validation**:
   - Run an automated validator across the entire build tree to detect and eliminate any dangling symlinks.
5. **Theme Index & Metadata**:
   - Generate a valid, complete `index.theme` declaring all actual contexts, sizes, and `ScaledDirectories`.
   - Ensure `Inherits=breeze-dark,breeze,hicolor`.
   - Generate `icon-theme.cache` via `gtk-update-icon-cache`.
6. **Verification & Testing**:
   - Review file counts, visual consistency, and verify with KDE Plasma settings.

---

## 7. Plasma 6 System Settings Icon Regression Resolution

### Root Cause Analysis
During initial deployment, multiple sidebar items in KDE Plasma System Settings (e.g., *Text & Fonts*, *Animations*, *Default Applications*, *Notifications*) defaulted to a squircle slider icon (pink/teal diagonal split with sliders).

The root causes were identified as:
1. **Invalid XDG Context Declarations**: In `index.theme`, `preferences/*` were declared as `Context=Preferences` and `apps/128`, `apps/256` as `Context=Apps`. Neither `Preferences` nor `Apps` are valid XDG contexts in KDE Frameworks (`KIconThemes`). KDE discarded those directories entirely (`kf.iconthemes: Invalid Context= "Preferences"`).
2. **Rogue Squircle in `apps/`**: Upstream `Chameleon` / `Breeze_Dark_RC` dumped a squircle slider icon as `apps/48/preferences-desktop.svg` and symlinked 77 preferences entries to it. When `preferences/` was discarded, suffix-stripping fallback in `apps/48` matched this rogue squircle.
3. **Missing Plasma 6 Modules**: Plasma 6 settings modules like `preferences-desktop-animations.svg`, `preferences-desktop-keyboard-shortcut.svg`, and `preferences-system-disks.svg` were absent.
4. **Overwritten System Category**: `categories/32/applications-system.svg` was overwritten with the squircle slider instead of the official Breeze gear/cog.

### Applied Surgical Fix
1. **Corrected Contexts & Scalability in `index.theme`**:
   - All `preferences/*` set to `Context=Applications`.
   - `preferences/32` declared `Type=Scalable`, `MinSize=32`, `MaxSize=256` (matching official Breeze).
   - `apps/48` restricted to `MinSize=48`, `MaxSize=256`.
   - `apps/128` and `apps/256` corrected to `Context=Applications`.
2. **Purged Rogue Files from `apps/`**: Removed all `preferences-desktop*` SVGs and PNGs from `apps/` (keeping only `preferences-desktop-font-installer.svg`), removed `applications-system` from `apps/`, and purged 77 symlinks pointing to `preferences-desktop`.
3. **Restored Official Plasma 6 SVGs**:
   - Sourced missing module icons directly from `/usr/share/icons/breeze-dark/preferences/` (32, 24, 22, 16).
   - Restored official Breeze gear/cog to `categories/32/applications-system.svg` and `categories/24/`.
4. **Cache & Validation**: Pruned 201 dangling symlinks, synced to `~/.local/share/icons/Breeze-Dark-Rounded/`, regenerated GTK icon cache, and verified via `kiconfinder6` that all sidebar modules resolve to their dedicated SVGs with 0 context errors.
