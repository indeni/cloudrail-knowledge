from typing import List, Optional


class PrefixList:

    def __init__(self, pl_id: str, pl_name: str, cidr_list: List[str], region: str = None) -> None:
        self.pl_id: str = pl_id
        self.pl_name: str = pl_name
        self.service_name: str = pl_name.split(".")[-1]
        self.cidr_list: List[str] = cidr_list
        self.region: str = region

    def __str__(self) -> str:
        return self.pl_name


class PrefixLists:

    def __init__(self, region: str) -> None:
        self.region: str = region
        self.prefix_lists: List[PrefixList] = []

    def get_prefix_lists_by_service(self, aws_service_type: str) -> Optional[PrefixList]:
        for prefix_list in self.prefix_lists:
            if prefix_list.service_name.lower() == aws_service_type.lower():
                return prefix_list
        return None
