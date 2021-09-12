from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class PrivateConnectionData(DataClassJsonMixin):
    source: str
    destination: str
    value: any


@dataclass
class PublicConnectionData:
    instance_id: str
    value: any
