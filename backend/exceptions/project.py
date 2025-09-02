class NotProjectMemberError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class NotProjectOwner(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class NotTaskAssigneeError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)