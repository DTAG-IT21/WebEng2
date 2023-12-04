import json

from flask import Response


def response_body(data_dict, status=200):
    body = json.dumps(
        data_dict,
        indent=4,
        separators=(',', ': ')
    )
    return Response(body, status=status, mimetype="application/json")


def no_content():
    return Response(status=204)


def error_response(message, more_info, status=400):
    code = {
        400: "bad_request",
        401: "unauthorized",
        404: "not_found",
        500: "internal_server_error"
    }

    body = {

        "errors": [
            {
                "code": code[status],
                "message": message,
                "more_info": more_info
            }
        ]
    }
    return response_body(body, status=status)
