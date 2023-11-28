import json
import uuid

from flask import Response
import distutils

import database


def handle_get(include_deleted, storey_id):
    where = "True"
    if not include_deleted == "True":
        where = where + " and deleted_at is null"

    if storey_id is not None:
        where = where + " and storey_id = '" + storey_id + "'"

    rows = database.select("*", "rooms", where)

    response_dict = {
        "rooms": []
    }
    for row in rows:
        response_dict["rooms"].append({
            "id": row[0],
            "name": row[1],
            "storey_id": row[2]
        })

    response = (json.dumps(
        response_dict,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ))
    return Response(response, status=200, mimetype="application/json")


def handle_get_by_id(id):
    # TODO
    return


def handle_post(name, storey_id):
    storeys = database.select(storey_id, "storeys", "storey_id = {}".format(storey_id))
    if storey_id:
        rooms = database.select("name", "rooms", "name = {}".format(name))
        if not rooms:
            room_id = uuid.uuid4()
            database.insert("rooms", [room_id, name, storey_id, None])
            response = {
                "id": room_id,
                "name": name,
                "storey:id": storey_id
            }
            return Response(response, status=200)
        else:
            response = {
                "errors": [
                    {
                        "code": "bad_request",
                        "message": "Room name already in use",
                        "more_info": "The given room name is already in use"
                    }]
            }
        return Response(response, status=400, mimetype="application/json")
    else:
        response = {
            "errors": [
                {
                    "code": "bad_request",
                    "message": "Storey not found",
                    "more_info": "There is no storey with the given id"
                }]
        }
        return Response(response, status=400, mimetype="application/json")


def handle_put_by_id(id):
    # TODO
    return