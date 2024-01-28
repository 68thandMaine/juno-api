class ServiceException(Exception):
    """
    Class used to relay a failure message when a service in
    juno fails for some reason.
    """

    def __init__(self, message="Service operation failed"):
        self.message = message
        super().__init__(self.message)
