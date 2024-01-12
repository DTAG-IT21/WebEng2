import src.main.response_generator as response_generator
from src.DAO.building_dao import BuildingDAO
from src.DAO.storey_dao import StoreyDAO
from src.DAO.base import Session
from sqlalchemy import and_

session = Session()


def handle_get(include_deleted, building_id):

    if building_id:
        if include_deleted == "true":
            storeys = session.query(StoreyDAO) \
                .filter(StoreyDAO.building_id == building_id) \
                .all()
        else:
            storeys = session.query(StoreyDAO) \
                .filter(and_(StoreyDAO.deleted_at.is_(None),
                        StoreyDAO.building_id == building_id)) \
                .all()
    else:
        if include_deleted == "true":
            storeys = session.query(StoreyDAO) \
                .all()
        else:
            storeys = session.query(StoreyDAO) \
                .filter(StoreyDAO.deleted_at.is_(None)) \
                .all()

    output = [
        {"id": str(s.id), "name": s.name, "building_id": str(s.building_id)}
        for s in storeys
    ]

    return response_generator.response_body({"storeys": output})


def handle_post(name, building_id):
    if not building_id or not name:
        message = "Missing parameters"
        more_info = "Handed parameters not sufficient"
        return response_generator.error_response(message, more_info, 400)

    buildings = session.query(BuildingDAO).get(building_id)
    if buildings:
        storeys = session.query(StoreyDAO) \
            .filter(and_(StoreyDAO.building_id == building_id,
                         StoreyDAO.name == name)) \
            .all()
        if not storeys:
            new_storey = StoreyDAO(name=name, building_id=building_id, deleted_at=None)
            session.add(new_storey)

            response_body = {
                "id": str(new_storey.id),
                "name": new_storey.name,
                "storey_id": str(new_storey.building_id)
            }
            session.commit()
            return response_generator.response_body(response_body)

        else:
            message = "Storey name already in use"
            more_info = "The given storey name is already in use"
            return response_generator.error_response(message, more_info, 400)

    else:
        message = "Building not found"
        more_info = "There is no building with the given id"
        return response_generator.error_response(message, more_info, 404)
