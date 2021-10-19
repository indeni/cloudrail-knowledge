from enum import Enum


class IgwType(str, Enum):
    IGW = "igw"
    EGRESS_ONLY_IGW = "egress_only_igw"
