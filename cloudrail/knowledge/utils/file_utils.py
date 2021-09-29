import functools
import hashlib
import json
import logging
import os
import shutil
from typing import List, Set
import requests
import rsa
import yaml
from cloudrail.knowledge.exceptions import ValidationException
from natsort import natsorted


def split(source: str, dest_folder: str, write_size_bytes: int) -> int:
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    os.mkdir(dest_folder)
    files_parts = 0
    with open(source, 'rb') as input_file:
        while True:
            chunk = input_file.read(write_size_bytes)
            # End the loop if we have hit EOF
            if not chunk:
                break
            files_parts += 1
            file_name = os.path.join(dest_folder, ('part_{}'.format(files_parts)))
            with open(file_name, 'wb') as dest_file:
                dest_file.write(chunk)
    return files_parts


def join(source_dir: str, dest_file: str, read_size_bytes: int):
    parts = os.listdir(source_dir)
    sorted_parts = natsorted(parts)
    with open(dest_file, 'wb') as output_file:
        for file in sorted_parts:
            path = os.path.join(source_dir, file)
            with open(path, 'rb') as input_file:
                while True:
                    bytes_read = input_file.read(read_size_bytes)
                    # Break out of loop if we are at EOF
                    if not bytes_read:
                        break
                    output_file.write(bytes_read)


@functools.lru_cache(maxsize=None)
def read_all_text(file_path: str, mode='r'):
    try:
        with open(file_path, mode) as file:
            return file.read()
    except Exception as ex:
        message = f'error while read text file {file_path}. {ex}'
        logging.exception(message)
        raise Exception(message)


@functools.lru_cache(maxsize=None)
def file_to_yaml(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as ex:
        message = f'error while read yaml file {file_path}. {ex}'
        logging.exception(message)
        raise Exception(message)


def get_all_files(path: str, exclude_dirs: Set[str] = None) -> List[str]:
    exclude_dirs = exclude_dirs or set()
    found_files = []
    for root, _, files in os.walk(path):
        if any(exclude_dir for exclude_dir in exclude_dirs if exclude_dir in root):
            continue
        for file_name in files:
            found_files.append(os.path.join(root, file_name))
    return found_files


def download_file(file_url: str, file_path: str):
    req = requests.get(file_url)
    with open(file_path, 'wb') as file:
        file.write(req.content)
    os.chmod(file_path, 0o777)


def verify_md5(file_path: str, md5_path: str):
    file_content = read_all_text(file_path, mode='rb')
    md5_hash = hashlib.md5()
    md5_hash.update(file_content)
    actual_md5 = md5_hash.hexdigest()
    md5_content = read_all_text(md5_path, mode='r')
    expected_md5 = md5_content.split(" ")[0]
    if actual_md5 != expected_md5:
        raise ValidationException('md5 validation failed')


def verify_rsa(file_path: str, rsa_path: str):
    pulic_key_data = '''-----BEGIN RSA PUBLIC KEY-----
MIICCgKCAgEAnTd+lJr9ImEVgBQG/HCtD50yI8hxaQRUnLXOL6c+hBqmh3/rD+bB
q7X+kssBNWyELOyLQgs+wxZNb9U7i4sD/4IK7ela7LEIS+Rd2xEQO2JhOKjaqG+v
oZ+MOcASZsQd7C04t9UWxAywZ7r0xcJ7HO34zpOBtPwcVpY/SvA2YU+yBhpu2MDw
Kk/o8YB/JpjhfbeTk83pTf0Q1ZZFOpEc5OpPAyrNo6Ou8bp2YBC4wHCIzSSvpOGJ
xMsBJYq3FKB5n8ZmKFXYiHHsriGmrypAPum7Em/ihiLQx2dsOkkAvn8V+Op1vmV2
wrKG4IvZoRLR+D9JQELmBPV+Fuww9TJmB5MtjJoyPdLIcXxImVR47zczJX4wOdZE
mlJ9u3Y5sbGCgPonruMFfbLDgXs9w3kvW6IaBkHudeQglmiBv6yorLm4hNk5ym1m
2X+JUKZ3r7YBiJWQ3kVSpGS2lLNgx8YCKdFF/sHKBbop7vSH6nY0TioaAwEmbLS5
vGtpjdMIbe4edTXPDyDQzPz9M77MJRY0WxDqvXYbdS0jztjs2dbSytFqvsl6tzaB
rmHw1MUAyhRdCe5k5356ccFWbckFuTHwAEtvzAHSEZncCMyNV+KfSzlkp8JH//jd
jUdrLxsYYdWbG7dllmy2pf2GDFxqvH2Jd43KP4rJae7xjR+jTJ8uolECAwEAAQ==
-----END RSA PUBLIC KEY-----'''
    public_key = rsa.PublicKey.load_pkcs1(pulic_key_data, 'PEM')
    file_content = read_all_text(file_path, mode='rb')
    rsa_content = read_all_text(rsa_path, mode='rb')
    if not rsa.verify(file_content, rsa_content, public_key):
        raise ValidationException('rsa validation failed')


def safe_delete(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


def download_signed_file(file_url: str, file_path: str, retry: bool = True):
    md5_path = ''
    rsa_path = ''
    try:
        if not os.path.isfile(file_path):
            download_file(file_url, file_path)
        md5_url = f'{file_url}.md5'
        md5_path = f'{file_path}.md5'
        if not os.path.isfile(md5_path):
            download_file(md5_url, md5_path)
        rsa_url = f'{md5_url}.rsa'
        rsa_path = f'{md5_path}.rsa'
        if not os.path.isfile(rsa_path):
            download_file(rsa_url, rsa_path)
        verify_md5(file_path, md5_path)
        verify_rsa(md5_path, rsa_path)
    except ValidationException as ex:
        logging.exception(f'validation of {file_path} failed')
        if retry:
            safe_delete(file_path)
            safe_delete(md5_path)
            safe_delete(rsa_path)
            download_signed_file(file_url, file_path, False)
        else:
            raise ex


def write_to_file(file_path: str, content: str):
    with open(file_path, 'w') as file:
        file.write(content)


def file_to_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def raise_file_format_mismatch(file: str):
    raise Exception(f'file format mismatch, file="{file}"')


def validate_file_exist(file_path: str):
    if not os.path.exists(file_path):
        raise Exception(f'file={file_path} don\'t exist')
