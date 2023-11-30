import json

from flask import Response


def response_body(data_dict, status=200):
    body = json.dumps(
        data_dict,
        indent=4,
        separators=(',', ': ')
    )
    return Response(body, status=status, mimetype="application/json")


def no_content(status=204):
    return Response(status=status)


def error_response(message, more_info, status=400):
    code = {
        400: "bad_request",
        401: "unauthorized",
        404: "not_found"
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
