class NotReachableException(Exception):
    def __init__(self, message="Cette géométrie n'est pas réalisable pour le robot."):
        self.message = message
        super().__init__(message)
