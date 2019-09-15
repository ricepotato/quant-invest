
class APIError(Exception):
    pass

class NotFound(APIError):
    pass

class BadRequest(APIError):
    pass