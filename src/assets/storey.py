import uuid

import src.main.database as database
import src.main.response_generator as response_generator


def handle_get(include_deleted, building_id):

    where_clause = "True"
    if include_deleted != "True":
        where_clause += " and deleted_at is null"

    if building_id is not None:
        where_clause += f" and building_id = '{building_id}'"

    rows = database.select("id, name, building_id", "storeys", where_clause)

    storeys = [
        {"id": storey_id, "name": name, "building_id": building_id}
        for storey_id, name, building_id in rows
    ]

    return response_generator.response_body({"storeys": storeys})


def handle_post(name, building_id):

    if building_id is None or name is None:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

    buildings = database.select("id", "buildings", f"id = '{building_id}'")
    if buildings:
        storeys = database.select("name", "storeys", f"building_id = '{building_id}' and name = '{name}'")
        if not storeys:
            storey_id = uuid.uuid4()
            database.insert("storeys", f"'{storey_id}', '{name}', '{building_id}', Null")

            response_body = {
                "id": str(storey_id),
                "name": name,
                "storey_id": str(building_id)
            }
            return response_generator.response_body(response_body)

        else:
            message = "Storey name already in use"
            more_info = "The given storey name is already in use"
            return response_generator.error_response(message, more_info, 400)

    else:
        message = "Building not found"
        more_info = "There is no building with the given id"
        return response_generator.error_response(message, more_info, 404)
