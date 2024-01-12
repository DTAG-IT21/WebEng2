import datetime

from sqlalchemy import and_

import src.main.response_generator as response_generator
from src.DAO.base import Session
from src.DAO.room_dao import RoomDAO
from src.DAO.storey_dao import StoreyDAO

session = Session()


def handle_get(room_id):
    room = session.query(RoomDAO).get(room_id)
    if not room:
        message = "Room not found",
        more_info = "No room with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": str(room.id), "name": room.name, "storey_id": str(room.storey_id)}
    return response_generator.response_body(response_body)


def handle_put(room_id, name, storey_id, deleted_at):
    # Check if storey not deleted
    storey = session.query(StoreyDAO).get(storey_id)
    if not storey:
        message = "storey not found"
        more_info = "The requested storey does not exist. Maybe it was deleted?"
        return response_generator.error_response(message, more_info, status=404)

    # Check if room name is already in use
    existing_room = session.query(RoomDAO) \
        .filter(and_(RoomDAO.name == name,
                     RoomDAO.storey_id == storey_id)) \
        .first()

    if existing_room and (str(existing_room.id) != str(room_id) or existing_room.deleted_at is None):
        message = "room name already used"
        more_info = "The given room name is already in use in the specified storey"
        return response_generator.error_response(message, more_info, status=400)

    room = session.query(RoomDAO).get(room_id)
    # Check if room exists
    if room:
        # Check if room was deleted
        if room.deleted_at is not None:
            # Check if room shall be restored
            if deleted_at is None:
                room.name = name
                room.building_id = storey_id
                room.deleted_at = None

                response_body = {
                    "id": str(room_id),
                    "name": name,
                    "building_id": str(storey_id)
                }
                session.commit()
                return response_generator.response_body(response_body)
            else:
                message = "room not found"
                more_info = "room not found or deleted. If you want to restore the room, pass deleted_at: null."
                return response_generator.error_response(message, more_info, status=404)
        # Check if the room shall be restored (although not deleted)
        elif deleted_at is None:
            message = "Bad Request"
            more_info = "room cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        # Update room
        else:
            room.name = name
            room.storey_id = storey_id

            response_body = {
                "id": str(room_id),
                "name": name,
                "storey_id": str(storey_id)
            }
            session.commit()
            return response_generator.response_body(response_body)
    else:
        message = "room not found"
        more_info = "room not found or deleted. If you want to restore the room, pass deleted_at: null."
        return response_generator.error_response(message, more_info, status=404)


def handle_delete(room_id):
    room = session.query(RoomDAO).get(room_id)
    if room.deleted_at is None:
        room.deleted_at = datetime.datetime.now()
        session.commit()
        return response_generator.no_content()
    else:
        message = "Room not found"
        more_info = "The requested room does not exist. Maybe it was already deleted?"
        return response_generator.error_response(message, more_info, 404)
