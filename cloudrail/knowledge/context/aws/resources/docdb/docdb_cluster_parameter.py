class DocDbClusterParameter:

    def __init__(self,
                 parameter_name: str,
                 parameter_value: str):
        self.parameter_name: str = parameter_name
        self.parameter_value: str = parameter_value
