import os
import shutil

from python_terraform import Terraform

from cloudrail.knowledge.utils import file_utils

current_path = os.path.dirname(os.path.abspath(__file__))


def clean_apply():
    failed_destroy = []
    all_files = file_utils.get_all_files(os.path.join(current_path, '../aws/scenarios/cross_version'))
    scenario_files = [f for f in all_files if 'aurora/cluster_with_instances_and_tags' in f]
    index = 0
    for scenario_file in scenario_files[index:]:
        index = index + 1
        print(f'{index}/{len(scenario_files)}')
        scenario_folder = os.path.dirname(scenario_file)
        terraform = Terraform(working_dir=scenario_folder, terraform_bin_path='/usr/local/bin/terraform')
        try:
            print(f'running destroy for test case {scenario_folder}')
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

        except Exception as ex:
            print(f'fail running destroy for {scenario_folder} : {ex}')
            failed_destroy.append(scenario_folder)
    print(f'{len(failed_destroy)} scenarios failed:\n{failed_destroy}')


clean_apply()
