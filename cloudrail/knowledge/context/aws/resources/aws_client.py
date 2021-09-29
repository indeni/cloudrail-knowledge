from abc import abstractmethod
from typing import Optional

from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.iam.role import Role


class AwsClient(ConnectionInstance):
    """
        every resource associated with role and
        can execute aws API calls should inherit from this class
        in order to attach the appropriate in/out bound connections (by connections builder)
    """
    def __init__(self) -> None:
        super().__init__()
        ConnectionInstance.__init__(self)
        self.iam_role: Optional[Role] = None

    @abstractmethod
    def get_id(self) -> str:
        pass
