import json
import os
import shutil

from dragoneye import AwsCloudScanSettings, AwsScanner, AwsSessionFactory
from python_terraform import Terraform

from cloudrail.knowledge.utils import file_utils
from test.helpers.custom_terraform_helper import create_terraform_executor

# Notes about the script:
# 1. This script assume your 'terraform' execution command is simply the string: "terraform" in the command line (line 43).
# Else, you should change line 43 (terraform_bin_path='terraform'), and assign your local path to terraform bin folder.

current_path = os.path.dirname(os.path.abspath(__file__))


def collect_data():
    aws_settings = AwsCloudScanSettings(
        commands_path=os.path.join(current_path, '../../../../src/core/scan_commands/aws.yaml'),
        account_name='default', default_region='us-east-1', regions_filter=['us-east-1']
    )

    session = AwsSessionFactory.get_session(profile_name=None, region='us-east-1')  # Raises exception if authentication is unsuccessful
    aws_scan_output_directory = AwsScanner(session, aws_settings).scan()
    return aws_scan_output_directory


def create_data():
    failed_scenarios = []
    all_files = file_utils.get_all_files(os.path.join(current_path, '../drift/aws/scenarios/cross_version'))
    scenario_files = [f for f in all_files if 'cached_plan.json' in f and 'launch-template-using-tag-field' in f]
    index = 0
    for scenario_file in scenario_files:
        index = index + 1
        print(f'{index}/{len(scenario_files)}')
        scenario_folder = os.path.dirname(scenario_file)
        cached_plan_for_drift_path = os.path.join(scenario_folder, 'cached_plan_for_drift.json')
        account_data_for_drift_path = os.path.join(scenario_folder, 'account-data-for-drift')
        if os.path.isfile(cached_plan_for_drift_path):
            continue
        exception_raised = False
        terraform = Terraform(working_dir=scenario_folder, terraform_bin_path='terraform')
        try:
            print(f'running test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.init()
            if ret_code == 1:
                raise Exception('failed to run Terraform init. stdout: {} stderr:{}'.format(stdout, stderr))
            print(f'running plan for test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.plan(out='plan.out')
            if ret_code == 1:
                raise Exception('failed to run Terraform plan. stdout: {} stderr:{}'.format(stdout, stderr))
            print(f'running apply for test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.apply_cmd(auto_approve=True)
            if ret_code == 1:
                exception_raised = True
                raise Exception('failed to run Terraform apply. stdout: {} stderr:{}'.format(stdout, stderr))
            print(f'running second plan for test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.plan(out='plan.out')
            if ret_code == 1:
                exception_raised = True
                raise Exception('failed to run Terraform plan. stdout: {} stderr:{}'.format(stdout, stderr))
            custom_terraform = create_terraform_executor(scenario_folder)
            print(f'running show for test case {scenario_folder}')
            ret_code, out, _ = custom_terraform.show_cmd('plan.out',
                                                         json=True,
                                                         generate_id_from_address=True,
                                                         override_data_dir='.cloudrail')
            if len(json.loads(out[2:]).keys()) == 1:
                exception_raised = True
                raise Exception('Empty plan.json generated, something wrong with "show"')
            with open(cached_plan_for_drift_path, 'w') as file:
                file.write(out[2:])
            collected_data_dir = collect_data()
            if os.path.isfile(os.path.join(collected_data_dir, 'default/.DS_Store')):
                os.remove(os.path.join(collected_data_dir, 'default/.DS_Store'))
            with open(os.path.join(collected_data_dir, 'default/us-east-1/sts-get-caller-identity.json')) as account_id_file:
                account_id_data = json.load(account_id_file)
            account_id = account_id_data['Account']
            _replace_account_id(cached_plan_for_drift_path, account_id)
            _replace_account_id(collected_data_dir, account_id)
            shutil.move(collected_data_dir, account_data_for_drift_path)
            shutil.make_archive(account_data_for_drift_path, 'zip', account_data_for_drift_path)
            shutil.rmtree(account_data_for_drift_path)
            print(f'running destroy for test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.destroy_cmd(auto_approve=True)
            if ret_code == 1:
                raise Exception('failed to run Terraform destroy. stdout: {} stderr:{}'.format(stdout, stderr))
            os.remove(os.path.join(scenario_folder, 'plan.out'))
            os.remove(os.path.join(scenario_folder, 'terraform.tfstate'))
            os.remove(os.path.join(scenario_folder, 'terraform.tfstate.backup'))
            os.remove(os.path.join(scenario_folder, '.terraform.lock.hcl'))
            shutil.rmtree(os.path.join(scenario_folder, '.terraform'))
            shutil.rmtree(os.path.join(scenario_folder, '.cloudrail'))

        except Exception as ex:
            print(f'fail running for {scenario_folder} : {ex}')
            failed_scenarios.append(scenario_folder)
        if exception_raised:
            print(f'attempting to run destroy for test case {scenario_folder}')
            ret_code, stdout, stderr = terraform.destroy_cmd(auto_approve=True)
            if ret_code == 1:
                raise Exception('failed to run Terraform destroy. stdout: {} stderr:{}'.format(stdout, stderr))
            if os.path.isfile(os.path.join(scenario_folder, 'plan.out')):
                os.remove(os.path.join(scenario_folder, 'plan.out'))
            if os.path.isfile(os.path.join(scenario_folder, 'terraform.tfstate')):
                os.remove(os.path.join(scenario_folder, 'terraform.tfstate'))
            if os.path.isfile(os.path.join(scenario_folder, 'terraform.tfstate.backup')):
                os.remove(os.path.join(scenario_folder, 'terraform.tfstate.backup'))
            if os.path.isfile(os.path.join(scenario_folder, '.terraform.lock.hcl')):
                os.remove(os.path.join(scenario_folder, '.terraform.lock.hcl'))
            if os.path.isfile(os.path.join(scenario_folder, '.terraform')):
                shutil.rmtree(os.path.join(scenario_folder, '.terraform'))
            if os.path.isfile(os.path.join(scenario_folder, '.cloudrail')):
                shutil.rmtree(os.path.join(scenario_folder, '.cloudrail'))
    print(f'{len(failed_scenarios)} scenarios failed:\n{failed_scenarios}')


# pylint: disable=unused-variable
def _replace_account_id(working_dir: str, account_id: str):
    if 'cached_plan_for_drift.json' in working_dir:
        fpath = os.path.join('', working_dir)
        with open(fpath) as file:
            string = file.read()
        string = string.replace(account_id, '111111111111')
        with open(fpath, "w") as file:
            file.write(string)
    else:
        for dname, dirs, files in os.walk(working_dir):
            for fname in files:
                fpath = os.path.join(dname, fname)
                with open(fpath) as file:
                    string = file.read()
                string = string.replace(account_id, '111111111111')
                with open(fpath, "w") as file:
                    file.write(string)
                if account_id in fname:
                    modified_name = fname.replace(account_id, '111111111111')
                    os.rename(fpath, os.path.join(dname, modified_name))


create_data()
