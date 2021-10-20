from dataclasses import dataclass


@dataclass
class DocDbClusterParameter:
    parameter_name: str
    parameter_value: str
