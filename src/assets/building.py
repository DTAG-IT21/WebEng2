import uuid

import src.main.database as database
import src.main.response_generator as response_generator


def handle_get(include_deleted):

    where_clause = "True"
    if include_deleted != "True":
        where_clause += " and deleted_at is null"

    rows = database.select("id, name, address", "buildings", where_clause)

    buildings = [
        {"id": building_id, "name": name, "address": address}
        for building_id, name, address in rows
    ]

    return response_generator.response_body({"buildings": buildings})


def handle_post(name, address):

    if address is None or name is None:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

    buildings = database.select("name", "buildings", f"address = '{address}' and name = '{name}'")
    if not buildings:
        building_id = uuid.uuid4()
        database.insert("buildings", f"'{building_id}', '{name}', '{address}', Null")

        response_body = {
            "id": str(building_id),
            "name": name,
            "address": address
        }
        return response_generator.response_body(response_body)

    else:
        message = "Building name already in use"
        more_info = "The given building name is already in use"
        return response_generator.error_response(message, more_info, 400)
