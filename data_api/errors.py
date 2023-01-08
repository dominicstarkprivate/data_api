
class ContentTypeNotJsonError(Exception):
    """Error for the case where the content type is not a application/json.
    """
    pass


class DialogCustomerRelationError(Exception):
    """Error for when the relationship between dialogs and customers (each
    dialog is assigned to exactly one customer, but a customer can have more
    than one dialogs).
    """
    pass


class DialogNotFoundError(Exception):
    """
    Error for when a requested dialog does not exist in the database.
    """
    pass
