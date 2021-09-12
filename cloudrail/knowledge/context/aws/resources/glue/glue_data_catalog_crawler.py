from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlueCrawler(AwsResource):
    """
        Attributes:
            crawler_name: The name of the crawler.
            database_name: The name of the database.
            arn: The ARN of the crawler.
    """
    def __init__(self,
                 crawler_name: str,
                 database_name: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_GLUE_CRAWLER)
        self.crawler_name: str = crawler_name
        self.database_name: str = database_name
        if self.account:
            self.arn: str = f'arn:aws:glue:{self.region}:{self.account}:crawler/{self.crawler_name}'
        else:
            self.arn = None

    def get_keys(self) -> List[str]:
        return [self.crawler_name, self.account, self.region]

    def get_name(self) -> str:
        return self.crawler_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Glue crawler'
        else:
            return 'Glue crawlers'

    def get_cloud_resource_url(self) -> str:
        return '{0}glue/home?region={1}#crawler:name={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.crawler_name)

    @property
    def is_tagable(self) -> bool:
        return True
