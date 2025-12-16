import os
from pathlib import Path

import requests

from .constants import (
    DATA_CACHE_PATH,
    DATA_HYDROLIC_PATH,
    DATA_URL,
    FS1_PATH,
    PROFILE_PATH,
    PS2_PATH,
)


def download_data(url: str, destination: Path):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    with open(destination, "wb") as file:
        file.write(response.content)


def unzip_file(zip_path: Path, extract_to: Path):
    import zipfile

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def retrieve_pipeline():
    DATA_CACHE_PATH.mkdir(parents=True, exist_ok=True)
    DATA_HYDROLIC_PATH.mkdir(parents=True, exist_ok=True)

    zip_path = DATA_CACHE_PATH / "tmp_condition_monitoring_of_hydraulic_systems.zip"
    download_data(DATA_URL, zip_path)
    unzip_file(zip_path, DATA_HYDROLIC_PATH)
    os.remove(zip_path)


def check_data_exists() -> bool:
    required_files = [
        PS2_PATH,
        FS1_PATH,
        PROFILE_PATH,
    ]
    return all(file.exists() for file in required_files)


def auto_retrieve_data():
    if not check_data_exists():
        print("Data files not found. Retrieving data...")
        retrieve_pipeline()


if __name__ == "__main__":
    retrieve_pipeline()
