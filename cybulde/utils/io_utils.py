import os
from fsspec import AbstractFileSystem, filesystem
from typing import Any

GCS_PREFIX = "gs://"
GCS_file_system_NAME = "gcs"
LOCAL_file_system_NAME = "file"

def open_file(path: str, mode: str = "r") -> Any:
    file_system = choose_file_system(path)
    return file_system.open(path, mode)

def choose_file_system(path: str) -> AbstractFileSystem:
    return filesystem(GCS_file_system_NAME) if path.startswith(GCS_PREFIX) else filesystem(LOCAL_file_system_NAME)

def is_dir(path: str) -> bool:
    file_system = choose_file_system(path)
    is_dir: bool = file_system.isdir(path)
    return is_dir


def is_file(path: str) -> bool:
    file_system = choose_file_system(path)
    is_file: bool = file_system.isfile(path)
    return is_file


def make_dirs(path: str) -> None:
    file_system = choose_file_system(path)
    file_system.makedirs(path, exist_ok=True)


def list_paths(path: str) -> list[str]:
    file_system = choose_file_system(path)
    if not is_dir(path):
        return []
    paths: list[str] = file_system.ls(path)
    if GCS_file_system_NAME in file_system.protocol:
        gs_paths: list[str] = [f"{GCS_PREFIX}{path}" for path in paths]
        return gs_paths
    return paths


def copy_dir(source_dir: str, target_dir: str) -> None:
    if not is_dir(target_dir):
        make_dirs(target_dir)
    source_files = list_paths(source_dir)
    for source_file in source_files:
        target_file = os.path.join(target_dir, os.path.basename(source_file))
        if is_file(source_file):
            with open_file(source_file, mode="rb") as source, open_file(target_file, mode="wb") as target:
                content = source.read()
                target.write(content)
        else:
            raise ValueError(f"Source file {source_file} is not a file.")
