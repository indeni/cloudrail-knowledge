from dataclasses import dataclass
from typing import Dict

import backoff
import requests
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixLists, PrefixList


@dataclass
class ServiceIpRange:
    ip_prefix: str
    region: str
    service: str
    network_border_group: str


class ServiceIpRangeBuilder:

    @staticmethod
    def to_prefix_lists() -> Dict[str, PrefixLists]:
        ip_ranges = ServiceIpRangeBuilder._get_services_ip_ranges_map()
        region_to_prefix_lists_map: Dict[str, PrefixLists] = {}
        for prefix in ip_ranges["prefixes"]:
            region: str = prefix["region"]
            service_name: str = prefix["service"]
            ip_prefix: str = prefix["ip_prefix"]
            if region not in region_to_prefix_lists_map:
                region_to_prefix_lists_map[region] = PrefixLists(region)
            prefix_list: PrefixList = region_to_prefix_lists_map[region].get_prefix_lists_by_service(service_name)
            if prefix_list:
                prefix_list.cidr_list.append(ip_prefix)
            else:
                prefix_list: PrefixList = ServiceIpRangeBuilder._create_fake_prefix_list(service_name, region)
                prefix_list.cidr_list.append(ip_prefix)
                region_to_prefix_lists_map[region].prefix_lists.append(prefix_list)
        return region_to_prefix_lists_map

    @staticmethod
    def _create_fake_prefix_list(service_name: str, region: str) -> PrefixList:
        return PrefixList(pl_id=f"pl-psuedo-{service_name.lower()}-{region}", pl_name=f"com.amazonaws.{region}.{service_name.lower()}",
                          cidr_list=[], region=region)

    @staticmethod
    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def _get_services_ip_ranges_map():
        url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
        return requests.get(url, allow_redirects=True).json()
