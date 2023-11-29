import uuid

import database
import response_generator


def handle_get(include_deleted, storey_id):

    where_clause = "True"
    if include_deleted != "True":
        where_clause += " and deleted_at is null"

    if storey_id is not None:
        where_clause += f" and storey_id = '{storey_id}'"

    rows = database.select("id, name, storey_id", "rooms", where_clause)

    rooms = [
        {"id": room_id, "name": name, "storey_id": storey_id}
        for room_id, name, storey_id in rows
    ]

    return response_generator.create_response({"rooms": rooms})


def handle_post(name, storey_id):

    if storey_id is None or name is None:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

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
            return response_generator.create_response(response_body)

        else:
            message = "Room name already in use",
            more_info = "The given room name is already in use"
            return response_generator.error_response(message, more_info, 400)

    else:
        message = "Storey not found"
        more_info = "There is no storey with the given id"
        return response_generator.error_response(message, more_info, 400)
