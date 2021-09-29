from typing import Dict, List

from cloudrail.knowledge.context.base_environment_context import CheckovResult


def to_checkov_results(dic: Dict[str, List[dict]]) -> Dict[str, List[CheckovResult]]:
    if dic:
        return {key: [CheckovResult.from_dict(result) for result in check_results] for (key, check_results) in dic.items()}
    else:
        return {}
