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