import copy
import functools
import json
import logging
import os
import random
import uuid
from functools import reduce
from multiprocessing.pool import Pool
from typing import Iterable, List, Callable, Iterator, Optional, Tuple
from pathlib import Path

from netaddr import IPNetwork, IPSet, AddrFormatError, valid_ipv4, valid_ipv6


PUBLIC_IP_MIN_FIRST_OCTET = 11
PUBLIC_IP_MAX_FIRST_OCTET = 171


# --- Dragoneye auxiliary utils
def get_nested_value(dictionary: dict, outer: str, inner: str):
    outer_json = dictionary.get(outer, None)
    if outer_json is not None:
        return outer_json.get(inner, None)
    return None


def remove_range_from_ip_ranges(ranges: list, remove_range: (int, int)):
    ranges = copy.copy(ranges)
    for from_ip, to_ip in ranges:
        if from_ip > remove_range[1]:
            break
        if to_ip < remove_range[0]:
            break
        if from_ip <= remove_range[0] and to_ip <= remove_range[1]:
            break

    ordered_ranges = sorted(ranges)
    return reduce(
        lambda acc, el: acc[:-1:] + [(min(*acc[-1], *el), max(*acc[-1], *el))]
        if acc[-1][1] >= el[0] - 1
        else acc + [el],
        ordered_ranges[1::],
        ordered_ranges[0:1],
    )


@functools.lru_cache(maxsize=None)
def get_account_names(path: str) -> List[str]:
    return get_subfolder_names(path)


@functools.lru_cache(maxsize=None)
def get_regions(path: str, account_name: str) -> List[str]:
    return get_subfolder_names(os.path.join(path, account_name))


@functools.lru_cache(maxsize=None)
def get_account_id(account_data_dir: str) -> str:
    filename = 'sts-get-caller-identity.json'
    filepath = None
    for root, _, files in os.walk(account_data_dir):
        if filename in files:
            filepath = os.path.join(root, filename)
            break

    if filepath is None:
        raise Exception(f'Cannot find {filename} under {account_data_dir}')

    return load_as_json(filepath)['Account']


@functools.lru_cache(maxsize=None)
def gcp_get_project_id(account_data_dir: str) -> str:
    filename = 'cloudresourcemanager-v3-projects-get.json'
    filepath = None
    for root, _, files in os.walk(account_data_dir):
        if filename in files:
            filepath = os.path.join(root, filename)
            break

    if filepath is None:
        raise Exception(f'Cannot find {filename} under {account_data_dir}')

    return load_as_json(filepath)['value'][0]['projectId']


# --- FILE SYSTEM UTILS
def get_subfolder_names(path: str):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def find_file(directory: str, file: str) -> str:
    path = next(x for x in Path(directory).rglob(file)).resolve()
    return str(path)


def load_as_json(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as stream:
            return json.load(stream)
    except Exception as ex:
        logging.warning('failed load file {}, reason={}'.format(file_path, str(ex)), exc_info=1)
        return {}


# --- MULTIPROCESSING UTILS
MULTIPROCESSING_MODE = False


def set_multiprocessing_mode(enable: bool):
    global MULTIPROCESSING_MODE
    MULTIPROCESSING_MODE = enable


def run_multiprocess_starmap(function: Callable, iterator: Iterator, multiprocessing_mode: bool = False) -> list:
    if multiprocessing_mode or MULTIPROCESSING_MODE:
        with Pool() as pool:
            return pool.starmap(function, iterator)
    else:
        return [function(*args) for args in iterator]


def run_multiprocess_map(function: Callable, iterator: Iterator, multiprocessing_mode: bool = False) -> list:
    if multiprocessing_mode or MULTIPROCESSING_MODE:
        with Pool() as pool:
            return pool.map(function, iterator)
    else:
        return [function(arg) for arg in iterator]


# --- LIST UTILS

def _inner_flat_list(list_of_list, result: list):
    if list_of_list and isinstance(list_of_list[0], list):
        for single_entity in list_of_list:
            _inner_flat_list(single_entity, result)
    else:
        result.extend(list_of_list)


def flat_list(list_of_lists: List[list]) -> list:
    if list_of_lists and not isinstance(list_of_lists[0], list):
        return list_of_lists
    result = []
    _inner_flat_list(list_of_lists, result)
    return result


def hash_list(data: list) -> int:
    return hash(str(data))

def is_iterable_with_values(iterable: Iterable) -> bool:
    return any(x is not None for x in iterable)

# --- NETWORKING UTILS
def compare_prefix_length(cidr1: str, cidr2: str) -> int:
    prefix_length1 = cidr1.split('/')[1]
    prefix_length2 = cidr2.split('/')[1]

    if prefix_length1 == prefix_length2:
        return 0
    if prefix_length1 < prefix_length2:
        return -1
    return 1


@functools.lru_cache(maxsize=None)
def is_subset(src_cidr: str, dest_cidr: str) -> bool:
    try:
        src_network = IPNetwork(src_cidr)
        dest_network = IPNetwork(dest_cidr)
        return src_network in dest_network
    except AddrFormatError:
        return False


@functools.lru_cache(maxsize=None)
def has_intersection(cidr1: str, cidr2: str) -> bool:
    return _is_valid_cidr_block_set([cidr1, cidr2]) and not IPSet([cidr1]).isdisjoint(IPSet([cidr2]))


@functools.lru_cache(maxsize=None)
def get_cidr_subset(cidr1: str, cidr2: str) -> Optional[str]:
    if _is_valid_cidr_block_set([cidr1, cidr2]):
        ip_set1: IPSet = IPSet([cidr1])
        ip_set2: IPSet = IPSet([cidr2])
        if ip_set1.issubset(ip_set2):
            return cidr1
        elif ip_set1.issuperset(ip_set2):
            return cidr2
    return None


@functools.lru_cache(maxsize=None)
def get_overlap_cidr(cidr1: str, cidr2: str) -> IPSet:
    if _is_valid_cidr_block_set([cidr1, cidr2]):
        return IPSet([cidr2]) & (IPSet([cidr1]))
    else:
        return IPSet()


@functools.lru_cache(maxsize=None)
def get_cidrs_diff(cidr1: str, cidr2: str) -> IPSet:
    if _is_valid_cidr_block_set([cidr1, cidr2]):
        return IPSet([cidr1]) - (IPSet([cidr2]))
    else:
        return IPSet()


def is_ip_address(ip: str) -> bool:
    return valid_ipv4(ip) or valid_ipv6(ip)


def is_valid_cidr_block(cidr_block: str) -> bool:
    return _is_valid_cidr_block_set([cidr_block])


def _is_valid_cidr_block_set(cidr_block_set: List[str]) -> bool:
    try:
        IPSet(cidr_block_set)
        return True
    except Exception:
        return False


def generate_random_public_ipv4() -> str:
    return "{}.{}.{}.{}".format(random.randint(PUBLIC_IP_MIN_FIRST_OCTET, PUBLIC_IP_MAX_FIRST_OCTET), random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))


def is_public_ip_range(ip_range: str) -> bool:
    if is_valid_cidr_block(ip_range):
        destination_range = IPNetwork(ip_range)
        return destination_range not in IPNetwork("10.0.0.0/8") and \
               destination_range not in IPNetwork("172.16.0.0/12") and \
               destination_range not in IPNetwork("192.168.0.0/16")
    return False


def is_all_ips(ip_range: str) -> bool:
    return ip_range in ('0.0.0.0/0', '::/0')


def create_pseudo_id(prefix: str) -> str:
    return f'{prefix}-pseudo-{str(uuid.uuid4())}'


def str_to_bool(value: str) -> Optional[bool]:
    options: dict = {'true': True, 'y': True, '1': True, 'yes': True,
                     'false': False, 'n': False, '0': False, 'no': False
                     }
    return options.get(value.lower(), None)


def safe_json_loads(json_str: str) -> Optional[dict]:
    try:
        return json.loads(json_str)
    except Exception:
        return None


@functools.lru_cache(maxsize=None)
def normalize_port_range(from_port: int, to_port: int) -> (int, int):
    if from_port == -1 \
            or from_port is None \
            or to_port == -1 \
            or to_port is None \
            or to_port - from_port == 65535:
        return get_all_ports_range()
    else:
        return from_port, to_port


@functools.lru_cache(maxsize=None)
def get_all_ports_range() -> (int, int):
    return 0, 65535


def is_port_in_range(port_range_tuple: Tuple[int, int], port: int) -> bool:
    lower_port: int = port_range_tuple[0]
    upper_port: int = port_range_tuple[1]
    normalized_port_range = normalize_port_range(lower_port, upper_port)
    return normalized_port_range[0] <= port <= normalized_port_range[1]


def is_port_in_ranges(port_range_tuples: List[Tuple[int, int]], port: int) -> bool:
    for port_range_tuple in port_range_tuples:
        lower_port: int = port_range_tuple[0]
        upper_port: int = port_range_tuple[1]
        normalized_port_range = normalize_port_range(lower_port, upper_port)
        if normalized_port_range[0] <= port <= normalized_port_range[1]:
            return True
    return False


def is_first_octet_in_range(ip: str, _range: Tuple):
    if not is_ip_address(ip):
        return False
    first_octet = int(ip.split('.')[0])
    return first_octet in range(_range[0], _range[1])


def build_lambda_function_integration_endpoint_uri(region: str, lambda_arn: str) -> str:
    return f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
