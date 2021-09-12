from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class BillingMode(Enum):
    PROVISIONED = "PROVISIONED"
    PAY_PER_REQUEST = "PAY_PER_REQUEST"


class TableFieldType(Enum):
    BYTE = "B"
    NUMBER = "N"
    STRING = "S"


@dataclass
class TableField:
    """
        Attributes:
            name: The field's name.
            type: The field type (one of B for Byte, N for Number, S for String).
    """
    name: str
    type: TableFieldType


class DynamoDbTable(AwsResource):
    """
        Attributes:
            table_name: The name of the table.
            table_id: The ID of the table.
            table_arn: The ARN of the table.
            billing_mode: One of PROVISIONED or PAY_PER_REQUEST.
            partition_key: The partition key used.
            sort_key: The sort key used.
            write_capacity: The write capacity configured.
            read_capacity: The read capacity configured.
            fields_attributes: The list of table field attributes (may be empty).
            kms_key_id: The KMS key ID to use to encrypt this table, if one is used.
            kms_data: The actual KmsKey object referenced by the KMS ID.
            server_side_encryption: True if SSE is enabled.
    """
    def __init__(self, table_name: str, region: str, account: str, table_id: str, table_arn: str,
                 billing_mode: BillingMode, partition_key: str, server_side_encryption: bool, kms_key_id: str, sort_key: str = None,
                 write_capacity: int = 0, read_capacity: int = 0, fields_attributes: List[TableField] = None):
        super().__init__(account, region, AwsServiceName.AWS_DYNAMODB_TABLE,
                         AwsServiceAttributes(aws_service_type=AwsServiceType.DYNAMODB.value, region=region))
        self.table_name: str = table_name
        self.table_id: str = table_id
        self.table_arn: str = table_arn
        self.billing_mode: BillingMode = billing_mode
        self.partition_key: str = partition_key
        self.sort_key: str = sort_key
        self.write_capacity: int = write_capacity
        self.read_capacity: int = read_capacity
        if fields_attributes is None:
            self.fields_attributes: List[TableField] = []
        self.fields_attributes: List[TableField] = fields_attributes
        self.server_side_encryption: bool = server_side_encryption
        self.kms_key_id: Optional[str] = kms_key_id
        self.kms_data: Optional[KmsKey] = None

    def get_keys(self) -> List[str]:
        return [self.table_name, self.table_arn, self.table_id]

    def get_name(self) -> str:
        return self.table_name

    def get_arn(self) -> str:
        return self.table_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DynamoDB table'
        else:
            return 'DynamoDB tables'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}dynamodb/home?region={1}#tables:selected={2};tab=overview'\
            .format(self.AWS_CONSOLE_URL, self.region, self.table_name)

    @property
    def is_tagable(self) -> bool:
        return True
