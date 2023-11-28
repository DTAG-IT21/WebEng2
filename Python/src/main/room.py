import json

import database


def handle_get(include_deleted):

    conn = database.get_connection()

    if include_deleted == "True":
        query = "select * from rooms"
    else:
        query = "select * from rooms where deleted_at is null"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    response_dict = {
        "rooms": []
    }
    for row in rows:
        response_dict["rooms"].append({
            "id": row[0],
            "name": row[1],
            "storey_id": row[2]
        })

    response = (json.dumps(
        response_dict,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ))

    return response
