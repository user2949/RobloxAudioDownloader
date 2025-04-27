# Roblox Audio Downloader

A simple Python application that allows you to download audio assets from Roblox by providing your `.ROBLOSECURITY` cookie, a Place ID, and a list of Asset IDs. Features include:

- **Hidden Cookie Field**: Your `.ROBLOSECURITY` cookie is obscured by default, with an option to show it when needed.
- **Browse Asset IDs File**: Select a `.txt` file containing comma-separated Asset IDs to populate the input field.
- **Progress Indicator**: A progress bar displays download progress for all assets.
- **Easy Asset Retrieval**: Fetches asset names and locations via Roblox API and saves audio files locally as `.ogg`.

---

## Prerequisites

- Python 3.7 or newer
- `requests` library
- `Pillow` library

Install dependencies using pip:

```bash
pip install requests pillow
```

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3 installed and dependencies installed.
3. Run the application:

```bash
python main.py
```

> **Note:** Replace `main.py` with the name of your script file if different.

## Usage

1. Launch the application:
   ```bash
   python main.py
   ```
2. Enter your Roblox `.ROBLOSECURITY` cookie.
3. (Optional) Check **Show Roblox Cookie** to verify the cookie value.
4. Enter the Roblox Place ID.
5. Provide one or more Asset IDs, separated by commas.
   - Or click **Browse** to load Asset IDs from a `.txt` file (must be comma-separated).
6. Click **Download Audio** to start downloading.
7. Audio files will be saved in the `audio_files` directory with sanitized file names, each in `.ogg` format.

## Configuration

- File paths are relative to where the script is run.
- Downloaded audio files are saved under `audio_files/` directory.

## Troubleshooting

- **Invalid Cookie**: Ensure your `.ROBLOSECURITY` cookie is correct and active.
- **Missing Commas**: The Asset IDs file must contain IDs separated by commas (e.g., `12345,67890,13579`).
- **Network Errors**: Check your internet connection and Roblox API availability.

## License

This project is released under the [MIT License](LICENSE).

---

_By RoomGENERAT0R_
