import functools
import ipaddress
import random
from typing import Union, Tuple, List, Iterable, Optional

from netaddr import IPNetwork

from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings \
    import PublicAccessBlockSettings, PublicAccessBlockLevel, create_pseudo_access_block
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.utils.utils import hash_list


class HashableList(list):
    def __hash__(self) -> int:
        return hash_list(self)


class ResourcesAssignerUtil:

    @classmethod
    def get_account_access_block(cls, account_id: str,
                                 public_access_block_list: List[PublicAccessBlockSettings], region: str) -> PublicAccessBlockSettings:
        return cls._get_account_access_block(account_id, HashableList(public_access_block_list), region)

    @staticmethod
    @functools.lru_cache()
    def _get_account_access_block(a_id: str, access_block_list: HashableList, region: str) -> PublicAccessBlockSettings:
        for access_block in access_block_list:
            if access_block.access_level == PublicAccessBlockLevel.ACCOUNT and access_block.bucket_name_or_account_id == a_id:
                return access_block
        return create_pseudo_access_block(bucket_name_or_account_id=a_id,
                                          access_level=PublicAccessBlockLevel.ACCOUNT,
                                          account_id=a_id,
                                          region=region)

    @classmethod
    def get_account_owner(cls, account_id: str, acls: List[S3ACL]) -> Union[Tuple[str, str], None]:
        return cls._get_account_owner(account_id, HashableList(acls))

    @staticmethod
    @functools.lru_cache()
    def _get_account_owner(account_id: str, acls: HashableList) -> Union[Tuple[str, str], None]:
        for acl in acls:
            if acl.account == account_id and acl.owner_id and acl.owner_name:
                return acl.owner_id, acl.owner_name
        return None

    @staticmethod
    def get_default_vpc(vpcs: Iterable[Vpc], account: str, region: str) -> Optional[Vpc]:
        return next((vpc for vpc in vpcs if vpc.is_default and vpc.account == account and vpc.region == region), None)

    @staticmethod
    def get_random_ip_in_subnet(cidr: str) -> str:
        ip_net: IPNetwork = IPNetwork(cidr)
        return (ipaddress.IPv4Address(ip_net[0]) + random.randint(1, ip_net.size - 1)).__str__()

    @classmethod
    def clear_cache(cls):
        cls._get_account_access_block.cache_clear()
        cls._get_account_owner.cache_clear()
