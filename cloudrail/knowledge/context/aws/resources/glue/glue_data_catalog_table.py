from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlueDataCatalogTable(AwsResource):
    """
        Attributes:
            table_name: The name of the table.
            database_name: The name of the database.
    """

    def __init__(self,
                 table_name: str,
                 database_name: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_GLUE_CATALOG_TABLE)
        self.table_name: str = table_name
        self.database_name: str = database_name

    def get_keys(self) -> List[str]:
        return [self.table_name, self.account, self.region]

    def get_name(self) -> str:
        return self.table_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Glue Data Catalog table'
        else:
            return 'Glue Data Catalog tables'

    def get_cloud_resource_url(self) -> str:
        return '{0}glue/home?region={1}#table:catalog={2};name={3};namespace={4}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.account, self.table_name, self.database_name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'table_name': self.table_name,
                'database_name': self.database_name}
