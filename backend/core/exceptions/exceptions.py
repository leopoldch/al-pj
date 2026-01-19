class BusinessError(Exception):
    pass


class ResourceNotFound(BusinessError):
    pass


class CloudUploadError(BusinessError):
    pass


class InsufficientRights(BusinessError):
    pass
