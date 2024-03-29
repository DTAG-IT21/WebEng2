from sqlalchemy import and_

import src.main.response_generator as response_generator
from src.DAO.base import Session
from src.DAO.room_dao import RoomDAO
from src.DAO.storey_dao import StoreyDAO

session = Session()


def handle_get(include_deleted, storey_id):
    if storey_id:
        if include_deleted == "true":
            rooms = session.query(RoomDAO) \
                .filter(RoomDAO.building_id == storey_id) \
                .all()
        else:
            rooms = session.query(RoomDAO) \
                .filter(and_(RoomDAO.deleted_at.is_(None),
                             RoomDAO.storey_id == storey_id)) \
                .all()
    else:
        if include_deleted == "true":
            rooms = session.query(RoomDAO) \
                .all()
        else:
            rooms = session.query(RoomDAO) \
                .filter(RoomDAO.deleted_at.is_(None)) \
                .all()

    output = [
        {"id": str(room.id), "name": room.name, "storey_id": str(room.storey_id)}
        for room in rooms
    ]
    return response_generator.response_body({"rooms": output})


def handle_post(name, storey_id):
    if not storey_id or not name:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

    storeys = session.query(StoreyDAO).get(storey_id)
    if storeys:
        rooms = session.query(RoomDAO) \
            .filter(and_(RoomDAO.storey_id == storey_id,
                         RoomDAO.name == name)) \
            .all()

        if not rooms:
            new_room = RoomDAO(name=name, storey_id=storey_id, deleted_at=None)
            session.add(new_room)

            response_body = {
                "id": str(new_room.id),
                "name": new_room.name,
                "storey_id": str(new_room.storey_id)
            }
            session.commit()
            return response_generator.response_body(response_body)

        else:
            message = "Room name already in use"
            more_info = "The given room name is already in use"
            return response_generator.error_response(message, more_info, 400)

    else:
        message = "Storey not found"
        more_info = "There is no storey with the given id"
        return response_generator.error_response(message, more_info, 404)
