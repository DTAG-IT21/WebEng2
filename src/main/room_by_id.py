import database
import response_generator


def handle_get(room_id):

    room = database.select("id, name, storey_id", "rooms", f"id = '{room_id}'")
    if not room:
        message = "Room not found",
        more_info = "No room with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": room[0][0], "name": room[0][1], "storey_id": room[0][2]}
    return response_generator.response_body(response_body)


def handle_put(room_id, name, storey_id, deleted_at):
    # Check if storey not deleted
    storey = database.select("id, deleted_at", "storeys", f"id = '{storey_id}'")
    if not (storey and storey[0][1] is None):
        message = "Storey not found"
        more_info = "The requested storey does not exist. Maybe it was deleted?"
        return response_generator.error_response(message, more_info, status=404)

    # Check if room name is already in use
    existing_room = database.select("id, deleted_at", "rooms", f"name='{name}' and storey_id = '{storey_id}'")
    if existing_room and (existing_room[0][0] != room_id or existing_room[0][1] is None):
        message = "Room name already used"
        more_info = "The given room name is already in use in the specified storey"
        return response_generator.error_response(message, more_info, status=400)

    room = database.select("*", "rooms", f"id = '{room_id}' and storey_id = '{storey_id}'")
    # Check if room is deleted
    if room and room[0][3] is not None:
        # Check if room shall be restored
        if deleted_at is None:
            database.update("rooms",
                            f"id='{room_id}', name='{name}', storey_id='{storey_id}', deleted_at=null",
                            f"id='{room_id}' and storey_id='{storey_id}'")
            response_body = {
                "id": str(room_id),
                "name": name,
                "storey_id": str(storey_id)
            }
            return response_generator.response_body(response_body)
        else:
            message = "Room not found"
            more_info = "Room not found or deleted. If you want to restore the room, pass deleted_at: null."
            return response_generator.error_response(message, more_info, status=404)
    elif room:
        if deleted_at is None:
            message = "Bad Request"
            more_info = "Room cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        else:
            database.update("rooms",
                            f"id='{room_id}', name='{name}', storey_id='{storey_id}', deleted_at=null",
                            f"id='{room_id}' and storey_id='{storey_id}'")
            response_body = {
                "id": str(room_id),
                "name": name,
                "storey_id": str(storey_id)
            }
            return response_generator.response_body(response_body)
    else:
        message = "Bad Request"
        more_info = "Room cannot be restored, as it is not deleted"
        return response_generator.error_response(message, more_info, status=400)


def handle_delete(room_id):
    room = database.select("*", "rooms", f"id = '{room_id}' and deleted_at is null")
    if room:
        database.update("rooms",
                        f"id = '{room[0][0]}', name = {room[0][1]}, storey_id = '{room[0][2]}', deleted_at = CURRENT_TIMESTAMP",
                        f"id = '{room_id}'")
        return response_generator.no_content()
    else:
        message = "Room not found"
        more_info = "The requested room does not exist. Maybe it was already deleted?"
        return response_generator.error_response(message, more_info, 404)
