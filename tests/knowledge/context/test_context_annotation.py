from dataclasses import dataclass
from typing import Optional, Type
import os


@dataclass
class TestOptions:
    """
    Args:
        tf_version: Specify which version to run. If none supplied, will run on all tf_versions. should comply with Semantic Versioning 2.0.0
        If supplied empty string, will not run any tf scenario
        run_cloudmapper: Boolean to determine if should run test for cloudmapper
    """
    __test__ = False
    tf_version: Optional[str] = None
    run_cloudmapper: bool = True
    run_terraform: bool = True
    run_drift_detection: bool = True
    always_use_cache_on_jenkins: bool = False
    use_cached_plan_data_ratio: int = int(os.getenv("TESTS_CACHED_PLAN_RATIO", "100"))
    expected_exception: Type[Exception] = None
    use_state_file: bool = False
    run_latest_provider: bool = True
    cfn_template_params: Optional[dict] = None


def context(module_path: str, base_scanner_data_for_iac: Optional[str] = None, test_options: TestOptions = TestOptions()):
    def test_case_decorator(test_case_function):
        def test_case_executor(test_class_instance):
            test_class_instance.run_test_case(module_path, test_case_function, base_scanner_data_for_iac, test_options)

        return test_case_executor

    return test_case_decorator
