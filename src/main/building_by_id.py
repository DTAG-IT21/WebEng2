import database
import response_generator


def handle_get(building_id):

    building = database.select("id, name, address", "buildings", f"id = '{building_id}'")
    if not building:
        message = "Building not found",
        more_info = "No building with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": building[0][0], "name": building[0][1], "address": building[0][2]}
    return response_generator.response_body(response_body)


def handle_put(building_id, name, address, deleted_at):
    # Check if building name is already in use
    existing_building = database.select("id, deleted_at", "buildings", f"name='{name}' and address = '{address}'")
    if existing_building and (existing_building[0][0] != building_id or existing_building[0][1] is None):
        message = "Building name already used"
        more_info = "The given Building name is already in use"
        return response_generator.error_response(message, more_info, status=400)

    building = database.select("*", "buildings", f"id = '{building_id}' and address = '{address}'")
    # Check if building is deleted
    if building and building[0][3] is not None:
        # Check if building shall be restored
        if deleted_at is None:
            database.update("buildings",
                            f"id='{building_id}', name='{name}', address='{address}', deleted_at=null",
                            f"id='{building_id}' and address='{address}'")
            response_body = {
                "id": str(building_id),
                "name": name,
                "address": address
            }
            return response_generator.response_body(response_body)
        else:
            message = "Building not found"
            more_info = "Building not found or deleted. If you want to restore the building, pass deleted_at: null."
            return response_generator.error_response(message, more_info, status=404)
    elif building:
        if deleted_at is None:
            message = "Bad Request"
            more_info = "Building cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        else:
            database.update("buildings",
                            f"id='{building_id}', name='{name}', address='{address}', deleted_at=null",
                            f"id='{building_id}' and address='{address}'")
            response_body = {
                "id": str(building_id),
                "name": name,
                "address": address
            }
            return response_generator.response_body(response_body)


def handle_delete(building_id):
    building = database.select("*", "buildings", f"id = '{building_id}' and deleted_at is null")
    if building:
        database.update("buildings",
                        f"id = '{building[0][0]}', name = {building[0][1]}, address = '{building[0][2]}, deleted_at = CURRENT_TIMESTAMP",
                        f"id = '{building_id}'")
        return response_generator.no_content()
    else:
        message = "Building not found"
        more_info = "The requested building does not exist. Maybe it was already deleted?"
        return response_generator.error_response(message, more_info, 404)
