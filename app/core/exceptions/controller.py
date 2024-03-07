from sqlalchemy.orm.exc import NoResultFound

from app.core.lib.exceptions import ServiceException


class ControllerException(Exception):
    """
    Class used to relay a failure message when a controller catches an exception.
    """

    def __init__(self, detail="Controller operation failed", status_code=500):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def handle_generic_exception(exception: Exception, caller_name: str):
    raise ControllerException(
        detail=f"There has been an issue in {caller_name}: {exception}"
    ) from exception


async def handle_error_in_service(exception: ServiceException, caller_name: str):
    """
    Used when there is an error in a controller due to some issue in
    a service class.
    """
    raise ControllerException(
        detail=f"There was an issue in the service {caller_name} => {str(exception)}"
    ) from exception


async def handle_value_error_in_service(exception: ValueError):
    raise ControllerException(
        detail=f"There is an issue with a value: {str(exception)}"
    ) from exception


async def handle_not_found_exception(e: str):
    raise ControllerException(
        detail=f"There was nothing found during a search: {e}", status_code=412
    )
