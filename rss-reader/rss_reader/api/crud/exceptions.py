
class CrudError(Exception):
    """Base exception for all CRUD errors."""

    def __init__(self, details: str):
        self.details = details


class ObjectDoesNotExist(CrudError):
    """Object does not exist error."""

    def __init__(self, obj_type: str, obj_id: int):
        self.details = f"{obj_type} with ID {obj_id} does not exist."
