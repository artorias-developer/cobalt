#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Type, Dict, Any


T = TypeVar('T', bound='BaseDto')

class BaseDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        validate_assignment=False,
        validate_default=False
    )

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Converts a Python dict to a Pydantic model.

        Parameters:
        - data: Dict object.

        Returns:
        - Instance of the Dto class.
        """
        return cls.model_validate(data)