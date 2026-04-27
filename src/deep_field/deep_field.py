import re
from typing import Any, Dict, Union


class DeepField:
    def __init__(self, field_path: str) -> None:
        self.field_path = field_path
        self.field_structure = self.__build_structure(field_path)

    def extract(self, structure: Dict[str, Any]) -> Union[Dict[str, Any], list]:
        return self.__extract(structure, self.field_structure)

    def __build_structure(self, given_path: str) -> Union[str, int, Dict[Any, Any]]:
        array_matcher = re.search(r"^\.\[(?P<leaf>[^\]]+)\](?P<rest>.*)$", given_path)
        dot_matcher = re.search(r"^\.\{(?P<leaf>[^\}]+)\}(?P<rest>.*)$", given_path)
        standard_matcher = re.search(r"^\.(?P<leaf>[^\.]+)(?P<rest>.*)$", given_path)

        if array_matcher:
            leaf: Union[int, str] = int(array_matcher.group("leaf"))
            rest = array_matcher.group("rest")
            if rest == "":
                return leaf
            else:
                return {leaf: self.__build_structure(rest)}
        elif dot_matcher:
            leaf = dot_matcher.group("leaf")
            rest = dot_matcher.group("rest")
            if rest == "":
                return leaf
            else:
                return {leaf: self.__build_structure(rest)}
        elif standard_matcher:
            leaf = standard_matcher.group("leaf")
            rest = standard_matcher.group("rest")
            if rest == "":
                return leaf
            else:
                return {leaf: self.__build_structure(rest)}

        else:
            raise ValueError(
                f"Invalid field path: {given_path}, "
                f"unable to extract field while build {self.field_path}"
            )

    def __extract(
        self, structure: Any, field_structure: Any
    ) -> Union[Dict[str, Any], list]:
        if isinstance(field_structure, str):
            return {field_structure: structure[field_structure]}

        key, value = field_structure.popitem()
        if isinstance(key, int):
            return [self.__extract(structure[key], value)]
        return {key: self.__extract(structure[key], value)}
