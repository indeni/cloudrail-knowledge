from enum import Enum


class KeyManager(Enum):
    """
        Enum

        AWS - key is managed by AWS

        CUSTOMER - key is managed by the Customer

    """
    AWS = 'AWS'
    CUSTOMER = 'CUSTOMER'
