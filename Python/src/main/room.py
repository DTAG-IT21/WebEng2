import json
import uuid

from flask import Response

import database

def create_response(data_dict, status=200):
    response = json.dumps(
        data_dict,
        indent=4,
        separators=(',', ': ')
    )
    return Response(response, status=status, mimetype="application/json")

def handle_get(include_deleted, storey_id):
    where_clause = "True"
    if include_deleted != "True":
        where_clause += " and deleted_at is null"

    if storey_id is not None:
        where_clause += f" and storey_id = '{storey_id}'"

    rows = database.select("*", "rooms", where_clause)

    rooms = [
        {"id": id, "name": name, "storey_id": storey_id, "deleted_at": deleted_at} for id, name, storey_id, deleted_at in rows
    ]

    return create_response({"rooms": rooms})

def handle_post(name, storey_id):
    if storey_id is None or name is None:
        response_body = {
            "errors": [
                {
                    "code": "bad_request",
                    "message": "Missing parameters",
                    "more_info": "Handed parameters not sufficient"
                }
            ]
        }
        return create_response(response_body, 400)

    storeys = database.select("id", "storeys", f"id = '{storey_id}'")

    if storeys:
        rooms = database.select("name", "rooms", f"storey_id = '{storey_id}' and name = '{name}'")

        if not rooms:
            room_id = uuid.uuid4()
            database.insert("rooms", f"'{room_id}', '{name}', '{storey_id}', Null")

            response_body = {
                "id": str(room_id),
                "name": name,
                "storey_id": str(storey_id)
            }
            return create_response(response_body)

        else:
            response_body = {
                "errors": [
                    {
                        "code": "bad_request",
                        "message": "Room name already in use",
                        "more_info": "The given room name is already in use"
                    }
                ]
            }
            return create_response(response_body, 400)

    else:
        response_body = {
            "errors": [
                {
                    "code": "bad_request",
                    "message": "Storey not found",
                    "more_info": "There is no storey with the given id"
                }]
        }
        return create_response(response_body, 400)


def handle_get_by_id(id):
    # TODO
    return

def handle_put_by_id(id):
    # TODO
    return