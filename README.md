 # Hide DLC Blocks

This repository contains `generate_mod.py`, a small utility that scans Space Engineers `.sbc` definition files and generates a local mod that hides DLC items by setting their `Public` value to `false`.

## Download
The mod built by this script is available on the Steam Workshop:

https://steamcommunity.com/sharedfiles/filedetails/?id=2990811919

## Requirements

- Python 3.8+
- `lxml` (see `requirements.txt`)

Install dependencies with:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

The script supports interactive and non-interactive modes.

1) Interactive (prompts for the Space Engineers path):

```powershell
python generate_mod.py
```

2) Non-interactive (pass the Space Engineers install path):

```powershell
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers"
```

3) Test mode (prints the audit table without writing files):

```powershell
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers" --test
```

You can redirect the test output to a file to keep the audit report:

```powershell
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers" --test > audit_report.md
```

## Output

By default the generated mod is written to your local Space Engineers Mods folder under `%APPDATA%\SpaceEngineers\Mods\HideAllDLCBlocks\Data\CubeBlocks_Hidden.sbc`.

## Preserving specific DLCs (optional)

You can provide an optional second positional argument containing one or more DLC names to preserve (they will be excluded from removal). Provide a single name or a comma-separated list. The script comparison is case-insensitive and trims whitespace.

Examples:

```powershell
# Preserve a single DLC named "StylePack"
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers" "StylePack"

# Preserve multiple DLCs
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers" "StylePack, DecorativeBlocks"

# Test mode with preserved DLCs (no files written)
python generate_mod.py "D:\SteamLibrary\steamapps\common\SpaceEngineers" "StylePack" --test
```

Safety behavior: if you provide DLC name(s) but none of them are found while scanning the game's `.sbc` files, the script will treat the run as test-mode and will not write any files — this prevents accidental generation when the provided names are incorrect. If some provided names are found and others are not, the script will proceed but print a note listing the missing names.