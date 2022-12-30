
from models.pydantic_models.request.class_room import ClassRoomRequest
from models.sql_models.class_room import ClassRoom
import exception


def register_class_room(db, class_room_data: ClassRoomRequest):
    """This is the function for adding the class room"""
    class_room_data = ClassRoom(**class_room_data.dict())
    db.add(class_room_data)
    db.commit()
    db.refresh(class_room_data)
    return class_room_data

def get_class_room(**kwargs):

    if "db" in kwargs:
        db = kwargs["db"]
        if "class_room_id" in kwargs:
            class_room_id = kwargs["class_room_id"]
            list_of_class_rooms = db.get(ClassRoom, class_room_id)
            if list_of_class_rooms:
                return list_of_class_rooms
            else:
                exception.Exception_id_not_found('class room')

        if "limit" in kwargs and 'skip' in kwargs:
            limit = kwargs["limit"]
            skip = kwargs["skip"]
            list_of_class_rooms = db.query(ClassRoom).offset(skip).limit(limit).all()
        else:
            list_of_class_rooms = db.query(ClassRoom).all()
        return list_of_class_rooms
    else:
        exception.Exception_database_error()