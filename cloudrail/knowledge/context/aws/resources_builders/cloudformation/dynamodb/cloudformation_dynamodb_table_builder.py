from typing import Dict, Optional, List

from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import DynamoDbTable, TableField, TableFieldType, BillingMode
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationDynamoDbTableBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DYNAMODB_TABLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DynamoDbTable:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        table_name = self.get_property(properties, 'TableName', self.get_resource_id(cfn_res_attr))
        table_arn = build_arn('dynamodb', region, account, 'table', None, table_name)
        billing_mode: BillingMode = BillingMode.PROVISIONED
        if 'BillingMode' in properties:
            billing_mode = BillingMode(properties['BillingMode'])
        partition_key: str = ""
        sort_key: Optional[str] = None
        for key_attr in properties["KeySchema"]:
            if key_attr["KeyType"] == "HASH":
                partition_key = key_attr["AttributeName"]
            else:
                sort_key = key_attr["AttributeName"]
        server_side_encryption = False
        kms_key_id = None
        if 'SSESpecification' in properties:
            server_side_encryption = properties['SSESpecification']['SSEEnabled']
            if server_side_encryption:
                kms_key_id = self.get_encryption_key_arn(properties['SSESpecification'].get('KMSMasterKeyId'), account, region, DynamoDbTable)
        write_capacity: int = 0
        read_capacity: int = 0
        if "ProvisionedThroughput" in properties:
            write_capacity = properties["ProvisionedThroughput"]["WriteCapacityUnits"]
            read_capacity = properties["ProvisionedThroughput"]["ReadCapacityUnits"]
        fields: List[TableField] = [TableField(field_attr["AttributeName"], TableFieldType(field_attr["AttributeType"]))
                                    for field_attr in properties["AttributeDefinitions"]]
        return DynamoDbTable(account=account, region=region, table_name=table_name, table_arn=table_arn, billing_mode=billing_mode, partition_key=partition_key,
                             server_side_encryption=server_side_encryption, kms_key_id=kms_key_id, sort_key=sort_key, write_capacity=write_capacity,
                             read_capacity=read_capacity, fields_attributes=fields)
