from sqlalchemy import or_

import src.main.response_generator as response_generator
from src.DAO.base import Session
from src.DAO.building_dao import BuildingDAO

session = Session()


def handle_get(include_deleted):
    if include_deleted == "true":
        buildings = session.query(BuildingDAO).all()
    else:
        buildings = session.query(BuildingDAO) \
            .filter(BuildingDAO.deleted_at.is_(None)) \
            .all()

    output = [
        {"id": str(building.id), "name": building.name, "address": building.address}
        for building in buildings
    ]

    return response_generator.response_body({"buildings": output})


def handle_post(name, address):
    if address is None or name is None:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

    buildings = session.query(BuildingDAO) \
        .filter(or_(BuildingDAO.address == address,
                    BuildingDAO.name == name)) \
        .all()

    if not buildings:
        new_building = BuildingDAO(name=name, address=address, deleted_at=None)
        session.add(new_building)

        response_body = {
            "id": str(new_building.id),
            "name": name,
            "address": address
        }
        session.commit()
        return response_generator.response_body(response_body)

    else:
        message = "Building name or address already in use"
        more_info = "The given building name or address is already in use"
        return response_generator.error_response(message, more_info, 400)
