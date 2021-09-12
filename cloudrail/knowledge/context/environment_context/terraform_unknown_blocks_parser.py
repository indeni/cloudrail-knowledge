from typing import List

from cloudrail.knowledge.context.unknown_block import UnknownBlock, BlockType


class TerraformUnknownBlocksParser:

    @staticmethod
    def parse(resource_changes: list) -> List[UnknownBlock]:
        result = []
        for resource_change in resource_changes:
            if resource_change.get('mode') == 'data':
                result.append(UnknownBlock(BlockType.DATASOURCE, resource_change['address']))
        return result
