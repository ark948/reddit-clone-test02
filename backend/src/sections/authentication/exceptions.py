




class CustomException(Exception):
    """ Base class for all errors """
    pass




class InvalidToken(CustomException):
    """ User has provided an invalid or expired token """
    pass



class RevokedToken(CustomException):
    """ User has provided a token that has been revoked """
    pass



class AccessTokenRequired(CustomException):
    """ User has provided a refresh token when an access token is required """
    pass



class RefreshTokenRequired(CustomException):
    """ User has provided an access token when a refresh token is required """
    pass


class UserAlreadyExists(CustomException):
    """ User has provided an email for a user who already exists during sign up """
    pass



class InvalidCredentials(CustomException):
    """ User has provided wrong email or password during sign up or log on """
    pass



class InsufficientPermission(CustomException):
    """ User does not have neccessary permissions """
    pass


class UserNotFound(CustomException):
    """" User not found """
    pass



class AccountNotVerified(CustomException):
    """ User has not verified their account yet """
    pass
