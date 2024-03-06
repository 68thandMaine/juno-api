class ControllerException(Exception):
    """
    Class used to relay a failure message when a controller catches an exception.
    """

    def __init__(self, detail="Controller operation failed", status_code=500):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
