import datetime

import src.main.database as database
import src.main.response_generator as response_generator

import src.main.response_generator as response_generator
from src.DAO.building_dao import BuildingDAO
from src.DAO.room_dao import RoomDAO
from src.DAO.storey_dao import StoreyDAO
from src.DAO.base import Session
from sqlalchemy import and_

session = Session()


def handle_get(storey_id):

    storey = session.query(StoreyDAO).get(storey_id)

    if not storey:
        message = "storey not found",
        more_info = "No storey with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": str(storey.id), "name": storey.name, "building_id": str(storey.building_id)}
    return response_generator.response_body(response_body)


def handle_put(storey_id, name, building_id, deleted_at):
    # Check if building not deleted
    building = session.query(BuildingDAO).get(building_id)
    if not building:
        message = "building not found"
        more_info = "The requested building does not exist. Maybe it was deleted?"
        return response_generator.error_response(message, more_info, status=404)

    # Check if storey name is already in use
    existing_storey = session.query(StoreyDAO) \
    .filter(and_(StoreyDAO.name == name,
                 StoreyDAO.building_id == building_id)) \
    .first()

    if existing_storey and (str(existing_storey.id) != str(storey_id) or existing_storey.deleted_at is None):
        message = "storey name already used"
        more_info = "The given storey name is already in use in the specified building"
        return response_generator.error_response(message, more_info, status=400)

    updated_storey = session.query(StoreyDAO).get(storey_id)
    # Check if storey exists
    if updated_storey:
        # Check if storey was deleted
        if updated_storey.deleted_at is not None:
            # Check if storey shall be restored
            if deleted_at is None:
                updated_storey.name = name
                updated_storey.building_id = building_id
                updated_storey.deleted_at = None
                session.commit()

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
        # Check if the storey shall be restored (although not deleted)
        elif deleted_at is None:
            message = "Bad Request"
            more_info = "storey cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        # Update Storey
        else:
            updated_storey.name = name
            updated_storey.building_id = building_id
            session.commit()

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


def handle_delete(storey_id):
    storey = session.query(StoreyDAO) \
        .filter(and_(StoreyDAO.id == storey_id,
                     StoreyDAO.deleted_at.is_(None))) \
        .first()
    if storey:
        rooms = session.query(RoomDAO) \
            .filter(RoomDAO.storey_id == storey_id) \
            .all()
        if not rooms:
            storey.deleted_at = datetime.datetime.now()
            session.commit()
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
