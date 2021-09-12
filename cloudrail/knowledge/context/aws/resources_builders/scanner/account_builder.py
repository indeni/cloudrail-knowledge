import os
import logging
from typing import List

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.utils.utils import load_as_json, get_subfolder_names
from cloudrail.knowledge.context.aws.resources.account.account import Account


class AccountBuilder:
    def __init__(self, working_dir: str, salt: str):
        self.working_dir = working_dir
        self.salt = salt

    def build(self) -> AliasesDict[Account]:
        accounts: List[Account] = []

        for account_name in self._get_account_names():
            if os.path.exists(os.path.join(self.working_dir, account_name, 'us-east-1')):
                path = os.path.join(self.working_dir, account_name, 'us-east-1')
                account = load_as_json(os.path.join(path, 'sts-get-caller-identity.json'))['Account']
                account_attributes_json = load_as_json(os.path.join(path, 'ec2-describe-account-attributes.json'))
                if account_attributes_json:
                    account_attributes = account_attributes_json['AccountAttributes']
                    supported_platforms = next(x for x in account_attributes if x['AttributeName'] == 'supported-platforms')
                    supports_ec2_classic_mode = any(x['AttributeValue'] == 'EC2' for x in supported_platforms['AttributeValues'])
                else:
                    logging.warning('Could not determine this account\'s supported-platforms, and therefore this account will be considered '
                                    'as an account that does not support EC2-Classic platform')
                    supports_ec2_classic_mode = False

                accounts.append(Account(account, account_name, supports_ec2_classic_mode))

        return AliasesDict(*accounts)

    def _get_account_names(self) -> List[str]:
        return get_subfolder_names(self.working_dir)
