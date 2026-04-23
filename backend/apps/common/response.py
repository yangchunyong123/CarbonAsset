from rest_framework.response import Response


def ok(data=None, message="ok"):
    """Return a success response with unified payload."""
    return Response({"code": 0, "message": message, "data": data or {}})


def fail(message="error", code=50000, data=None, status=400):
    """Return an error response with unified payload."""
    return Response({"code": code, "message": message, "data": data or {}}, status=status)
