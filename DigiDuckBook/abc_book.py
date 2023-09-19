from abc import abstractmethod, ABC


class AbstractData(ABC):

    @abstractmethod
    def output_all_data(self) -> str | dict[str, str | list[str]] :
        pass