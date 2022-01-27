from http import HTTPStatus

def NoContent():
    return '', HTTPStatus.NO_CONTENT

def NotFound():
    return '', HTTPStatus.NOT_FOUND

def Unauthorized():
    return '', HTTPStatus.UNAUTHORIZED

def Forbidden():
    return '', HTTPStatus.FORBIDDEN

def Accepted():
    return '', HTTPStatus.ACCEPTED

def Created(obj):
    return obj, HTTPStatus.CREATED