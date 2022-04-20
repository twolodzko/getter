import collections.abc as abc
import inspect
from abc import ABC, abstractmethod
from typing import Any, Iterable, Mapping, NamedTuple, Optional, Union

MaybeNames = Optional[Union[Mapping[str, Any], Iterable[str]]]


class Parameter(NamedTuple):
    """
    Parameter has a name and optional default value
    """

    name: str
    default: Any

    @property
    def has_default(self) -> bool:
        return self.default is not inspect.Parameter.empty


class Getter(ABC):
    fields: Mapping[Parameter, Any]

    def __init__(
        self,
        params: Iterable[Parameter],
        names: MaybeNames = None,
    ) -> None:
        """
        Getter extracts the parameters from data

        :param params: list of the parameters to extract
        :param names: optional list of the names of the data fields
            or mappings from parameter names to names of the data fields
        :param useattr: read values from attributes, rather than fields of the object
        :raises ValueError: when names are inconsistent with the list of parameters
        """
        keys = self._names_to_keys(names)

        if keys is not None:
            try:
                self.fields = {param: keys[param.name] for param in params}
            except KeyError:
                raise ValueError("names do not contain mappings for all the parameters")
        else:
            self.fields = {param: param.name for param in params}

    def collect_from(self, obj) -> Mapping[str, Any]:
        """
        Extract parameters from an object and store as parameter name -> values mapping
        """

        collected = {}
        for param, key in self.fields.items():
            try:
                value = self._get(obj, key)
            except KeyError:
                if param.has_default:
                    value = param.default
                else:
                    raise

            collected[param.name] = value
        return collected

    @staticmethod
    def _names_to_keys(names: MaybeNames) -> Optional[Mapping[str, Any]]:
        """
        Parse names to an optional mapping name -> key in the data object
        """
        if names is None or isinstance(names, abc.Mapping):
            return names
        elif isinstance(names, abc.Iterable):
            return {name: i for i, name in enumerate(names)}
        else:
            raise TypeError

    @abstractmethod
    def _get(self, obj, key):
        ...


class ItemGetter(Getter):
    def _get(self, obj, key):
        return obj[key]


class AttributeGetter(Getter):
    def _get(self, obj, key):
        return getattr(obj, key)
