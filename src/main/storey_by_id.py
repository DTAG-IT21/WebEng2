import database
import response_generator


def handle_get(storey_id):

    storey = database.select("id, name, building_id", "storeys", f"id = '{storey_id}'")
    if not storey:
        message = "storey not found",
        more_info = "No storey with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": storey[0][0], "name": storey[0][1], "building_id": storey[0][2]}
    return response_generator.response_body(response_body)


def handle_put(storey_id, name, building_id, deleted_at):
    # Check if building not deleted
    building = database.select("id, deleted_at", "buildings", f"id = '{building_id}'")
    if not (building and building[0][1] is None):
        message = "building not found"
        more_info = "The requested building does not exist. Maybe it was deleted?"
        return response_generator.error_response(message, more_info, status=404)

    # Check if storey name is already in use
    existing_storey = database.select("id, deleted_at", "storeys", f"name='{name}' and building_id = '{building_id}'")
    if existing_storey and (existing_storey[0][0] != storey_id or existing_storey[0][1] is None):
        message = "storey name already used"
        more_info = "The given storey name is already in use in the specified building"
        return response_generator.error_response(message, more_info, status=400)

    storey = database.select("*", "storeys", f"id = '{storey_id}' and building_id = '{building_id}'")
    # Check if storey is deleted
    if storey and storey[0][3] is not None:
        # Check if storey shall be restored
        if deleted_at is None:
            database.update("storeys",
                            f"id='{storey_id}', name='{name}', building_id='{building_id}', deleted_at=null",
                            f"id='{storey_id}' and building_id='{building_id}'")
            response_body = {
                "id": str(storey_id),
                "name": name,
                "building_id": str(building_id)
            }
            return response_generator.response_body(response_body)
        else:
            message = "storey not found"
            more_info = "storey not found or deleted. If you want to restore the storey, pass deleted_at: null."
            return response_generator.error_response(message, more_info, status=404)
    elif storey:
        if deleted_at is None:
            message = "Bad Request"
            more_info = "storey cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        else:
            database.update("storeys",
                            f"id='{storey_id}', name='{name}', building_id='{building_id}', deleted_at=null",
                            f"id='{storey_id}' and building_id='{building_id}'")
            response_body = {
                "id": str(storey_id),
                "name": name,
                "building_id": str(building_id)
            }
            return response_generator.response_body(response_body)


def handle_delete(storey_id):
    storey = database.select("*", "storeys", f"id = '{storey_id}' and deleted_at is null")
    if storey:
        rooms = database.select("*", "rooms", f"storey_id = {storey_id}")
        if not rooms:
            database.update("storeys",
                            f"id = '{storey[0][0]}', name = {storey[0][1]}, building_id = '{storey[0][2]}, deleted_at = GETDATE()",
                            f"id = '{storey_id}'")
            return response_generator.no_content()
        else:
            message = "Storey cannot be deleted"
            more_info = ("The given storey still has active rooms. "
                         "Please delete all corresponding rooms before deleting the storey.")
            return response_generator.error_response(message, more_info, 400)
    else:
        message = "storey not found"
        more_info = "The requested storey does not exist. Maybe it was already deleted?"
        return response_generator.error_response(message, more_info, 404)
