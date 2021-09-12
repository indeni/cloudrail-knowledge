from abc import abstractmethod


class BaseScannerBuilder:
    @abstractmethod
    def do_build(self, attributes: dict):
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass
