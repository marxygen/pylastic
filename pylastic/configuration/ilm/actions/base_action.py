from abc import ABC, abstractmethod
from typing import List


class ILMAction(ABC):
	name: str  # Action name
	allowed_phases: List[str]  # List of phases in which this action is allowed (`hot`, `warm`, `cold`, `frozen`, `delete`)
	allowed_parameters: List[str] | None  # List of allowed parameters

	def __init__(self, **kwargs):
		"""
        Initialize this ILM Action.

        :param kwargs: Parameters (must be present in `allowed_parameters)
        """
		disallowed_parameters = [p for p in kwargs if p not in self.allowed_parameters]
		if disallowed_parameters:
			raise ValueError(f'Invalid parameter(s): {", ".join(disallowed_parameters)}')

		self.parameters = kwargs

	@abstractmethod
	def to_json(self) -> dict:
		"""Convert this action to a dictionary representing the request body"""
		raise NotImplementedError()
