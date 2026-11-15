"""Download raw data files (public, no registration). Sizes: MATR 4 files ~10.9 GB,
HUST zip ~1.2 GB. URLs are the ones used by Microsoft BatteryML
(github.com/microsoft/BatteryML, batteryml/preprocess/download.py)."""
import os
import subprocess
import zipfile

MATR = {
    "MATR_batch_20170512.mat": "https://data.matr.io/1/api/v1/file/5c86c0b5fa2ede00015ddf66/download",
    "MATR_batch_20170630.mat": "https://data.matr.io/1/api/v1/file/5c86bf13fa2ede00015ddd82/download",
    "MATR_batch_20180412.mat": "https://data.matr.io/1/api/v1/file/5c86bd64fa2ede00015ddbb2/download",
    "MATR_batch_20190124.mat": "https://data.matr.io/1/api/v1/file/5dcef152110002c7215b2c90/download",
}
HUST = ("hust_data.zip", "https://data.mendeley.com/public-files/datasets/nsc7hnsg4s/files/"
        "5ca0ac3e-d598-4d07-8dcb-879aa047e98b/file_downloaded")
EXPECTED_BYTES = {"MATR_batch_20170512.mat": 3025320241, "MATR_batch_20170630.mat": 2007331155,
                  "MATR_batch_20180412.mat": 3236690412, "MATR_batch_20190124.mat": 2601295745,
                  "hust_data.zip": 1188136932}


def _get(url, path):
    if os.path.exists(path) and os.path.getsize(path) == EXPECTED_BYTES.get(os.path.basename(path), -1):
        return
    subprocess.run(["curl", "-sS", "-L", "--retry", "5", "-C", "-", "-o", path, url], check=True)


def download_all(raw_root):
    os.makedirs(f"{raw_root}/MATR", exist_ok=True)
    os.makedirs(f"{raw_root}/HUST", exist_ok=True)
    for fn, url in MATR.items():
        _get(url, f"{raw_root}/MATR/{fn}")
    _get(HUST[1], f"{raw_root}/HUST/{HUST[0]}")
    out = f"{raw_root}/HUST/extracted"
    if not os.path.isdir(f"{out}/our_data"):
        zipfile.ZipFile(f"{raw_root}/HUST/{HUST[0]}").extractall(out)
    for fn, n in EXPECTED_BYTES.items():
        p = f"{raw_root}/MATR/{fn}" if fn.endswith(".mat") else f"{raw_root}/HUST/{fn}"
        assert os.path.getsize(p) == n, f"size mismatch for {p}"
