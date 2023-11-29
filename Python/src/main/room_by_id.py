import database
import response_generator


def handle_get(room_id):

    room = database.select("id, name, storey_id", "rooms", "id = " + str(room_id))
    if not room:
        message = "Room not found",
        more_info = "No room with the given id found"
        return response_generator.error_response(message, more_info, status=400)

    response_body = {"id": room[0][0], "name": room[0][1], "storey_id": room[0][2]}
    return response_generator.create_response(response_body)
