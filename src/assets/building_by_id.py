import datetime

from sqlalchemy import or_, and_

import src.main.response_generator as response_generator
from src.DAO.base import Session
from src.DAO.building_dao import BuildingDAO
from src.DAO.storey_dao import StoreyDAO

session = Session()


def handle_get(building_id):
    building = session.query(BuildingDAO).get(building_id)
    if not building:
        message = "Building not found",
        more_info = "No building with the given id found"
        return response_generator.error_response(message, more_info, status=404)

    response_body = {"id": str(building.id), "name": building.name, "address": building.address}
    return response_generator.response_body(response_body)


def handle_put(building_id, name, address, deleted_at):
    # Check if building name is already in use
    existing_buildings = session.query(BuildingDAO) \
        .filter(and_(or_(BuildingDAO.name == name,
                         BuildingDAO.address == address)),
                BuildingDAO.deleted_at.is_(None)) \
        .all()
    if existing_buildings:
        message = "Building name or address already used"
        more_info = "The given Building name or address are already in use"
        return response_generator.error_response(message, more_info, status=400)

    building = session.query(BuildingDAO).get(building_id)
    # Check if building exists
    if building:
        # Check if building is deleted
        if building.deleted_at:
            # Check if building shall be restored
            if not deleted_at:
                building.name = name
                building.address = address
                building.deleted_at = None

                response_body = {
                    "id": str(building.id),
                    "name": building.name,
                    "address": building.address
                }
                session.commit()
                return response_generator.response_body(response_body)
            else:
                message = "Building not found"
                more_info = "Building not found or deleted. If you want to restore the building, pass deleted_at: null."
                return response_generator.error_response(message, more_info, status=404)
        # Check if building shall be restored (although not deleted)
        elif not deleted_at:
            message = "Bad Request"
            more_info = "Building cannot be restored, as it is not deleted"
            return response_generator.error_response(message, more_info, status=400)
        else:
            building.name = name
            building.address = address

            response_body = {
                "id": str(building.id),
                "name": building.name,
                "address": building.address
            }
            session.commit()
            return response_generator.response_body(response_body)
    else:
        message = "Building not found"
        more_info = "Building not found or deleted. If you want to restore the building, pass deleted_at: null."
        return response_generator.error_response(message, more_info, status=404)


def handle_delete(building_id):
    building = session.query(BuildingDAO).get(building_id)
    if building and not building.deleted_at:
        storeys = session.query(StoreyDAO) \
            .filter(StoreyDAO.building_id == building_id) \
            .all()
        print(storeys)
        if not storeys:
            building.deleted_at = datetime.datetime.now()
            session.commit()
            return response_generator.no_content()
        else:
            message = "Building cannot be deleted"
            more_info = ("The given building still has active storeys. "
                         "Please delete all corresponding storeys before deleting the building.")
            return response_generator.error_response(message, more_info, 400)
    else:
        message = "Building not found"
        more_info = "The requested building does not exist. Maybe it was already deleted?"
        return response_generator.error_response(message, more_info, 404)
