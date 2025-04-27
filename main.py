import requests
import random
import time
import re
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from threading import Thread
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser

def download_icon(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)) if response.status_code == 200 else None

def sleep():
    time.sleep(0.01 + random.uniform(-0.001, 0.001))

def fetch_audio_location(asset_id, place_id, roblox_cookie):
    headers = {
        "User-Agent": "Roblox/WinInet",
        "Content-Type": "application/json",
        "Cookie": f".ROBLOSECURITY={roblox_cookie}",
        "Roblox-Place-Id": place_id,
    }
    body_array = [{"assetId": asset_id, "assetType": "Audio", "requestId": "0"}]
    while True:
        response = requests.post('https://assetdelivery.roblox.com/v2/assets/batch', headers=headers, json=body_array)
        if response.status_code == 200 and response.json()[0].get("locations"):
            return response.json()[0]["locations"][0]["location"]
        time.sleep(0.5)

def sanitize_filename(name):
    return re.sub(r'[\\/*?"<>|]', '', name.replace(" ", "_"))

def fetch_asset_name(asset_id):
    while True:
        response = requests.get(f"https://economy.roproxy.com/v2/assets/{asset_id}/details")
        if response.status_code == 200:
            return response.json().get("Name")
        time.sleep(0.5)

def download_audio_file(asset_id, place_id, roblox_cookie):
    asset_name = fetch_asset_name(asset_id)
    if asset_name:
        sanitized_name = sanitize_filename(asset_name)
        audio_url = fetch_audio_location(asset_id, place_id, roblox_cookie)
        if audio_url:
            response = requests.get(audio_url)
            if response.status_code == 200:
                os.makedirs("audio_files", exist_ok=True)
                file_path = os.path.join("audio_files", sanitized_name + ".ogg")
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            sleep()
                return True
    return False

def download_all_audio_files(roblox_cookie, place_id, asset_ids):
    total_assets = len(asset_ids)
    progress_bar['maximum'] = total_assets
    for asset_id in asset_ids:
        if download_audio_file(asset_id, place_id, roblox_cookie):
            progress_bar['value'] += 1
    messagebox.showinfo("Download Complete", "All audio assets have been downloaded.")

def start_download():
    roblox_cookie = cookie_entry.get()
    place_id = place_id_entry.get()
    asset_ids = asset_ids_entry.get().split(',')
    progress_bar['value'] = 0
    Thread(target=download_all_audio_files, args=(roblox_cookie, place_id, asset_ids)).start()

def open_link():
    webbrowser.open("https://www.youtube.com/watch?v=1v3inNUxyL8")

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        content = open(filename, "r").read().strip()
        if "," not in content:
            messagebox.showerror("Error", "File must contain comma-separated Asset IDs")
        else:
            asset_ids_entry.delete(0, tk.END)
            asset_ids_entry.insert(0, content)

root = tk.Tk()
root.title("Roblox Audio Downloader")
root.resizable(False, False)
root.attributes("-fullscreen", False)

icon_image = download_icon("https://i.gyazo.com/ef99bbd0561acbaa47394df9f03fc564.png")
if icon_image:
    root.iconphoto(True, ImageTk.PhotoImage(icon_image))

frame = ttk.Frame(root, padding="5")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)

labels_and_entries = [
    ("Roblox Cookie (.ROBLOSECURITY):", 0),
    ("Roblox Place ID:", 1),
    ("Asset IDs (comma-separated):", 2)
]

show_password_var = tk.BooleanVar()
def toggle_password():
    cookie_entry.config(show='' if show_password_var.get() else '•')

for text, idx in labels_and_entries:
    row = idx * 3
    ttk.Label(frame, text=text).grid(column=0, row=row, columnspan=3, sticky=tk.W, pady=2)
    if "Cookie" in text:
        cookie_entry = ttk.Entry(frame, width=50, show="•")
        cookie_entry.grid(column=0, row=row+1, columnspan=3, pady=2)
        ttk.Checkbutton(frame, text="Show Roblox Cookie", variable=show_password_var, command=toggle_password).grid(column=0, row=row+2, columnspan=3, pady=2)
    elif "Place ID" in text:
        place_id_entry = ttk.Entry(frame, width=50)
        place_id_entry.grid(column=0, row=row+1, columnspan=3, pady=2)
    else:
        asset_ids_entry = ttk.Entry(frame, width=50)
        asset_ids_entry.grid(column=0, row=row+1, columnspan=3, pady=2)
        ttk.Button(frame, text="Browse", command=browse_file).grid(column=1, row=row+2, pady=2)

ttk.Button(frame, text="Download Audio", command=start_download).grid(column=0, row=9, columnspan=3, sticky=tk.EW, pady=2)
progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=400)
progress_bar.grid(column=0, row=10, columnspan=3, sticky=(tk.W, tk.E), pady=2)
ttk.Button(frame, text="If you do not know how to get your .ROBLOSECURITY file, please watch the following video.", command=open_link).grid(column=0, row=11, columnspan=3, sticky=(tk.W, tk.E), pady=2)
ttk.Label(frame, text="By RoomGENERAT0R").grid(column=0, row=12, columnspan=3, pady=2)

root.mainloop()
