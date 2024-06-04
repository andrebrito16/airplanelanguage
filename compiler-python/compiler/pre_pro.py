class PreProcessing:
    def __init__(self) -> None:
        pass

    @staticmethod
    def filter(source: str) -> str:
        import re

        cleaned_source = re.sub(r"//.*|\n$", "", source)
        return cleaned_source
