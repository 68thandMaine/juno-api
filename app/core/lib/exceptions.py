from sqlalchemy.orm.exc import NoResultFound

_ = NoResultFound


class ServiceException(Exception):
    """
    Class used to
    relay a failure message when a service in
    juno fails for some reason.
    """

    def __init__(self, message="Service operation failed"):
        self.message = message
        super().__init__(self.message)


class ControllerException(Exception):
    """
    Class used to relay a failure message when a controller catches an exception.
    """

    def __init__(self, detail="Controller operation failed", status_code=500):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
