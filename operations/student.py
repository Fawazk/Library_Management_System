
from fastapi import HTTPException
from models.sql_models.students import Students
from sqlmodel import select
import exception
from models.pydantic_models.response.student import StudentResponse


def register_student(db, new_student_data):
    class_room_id = new_student_data.class_room
    student_name = new_student_data.name
    append_student_data = None
    student_name_list = []
    student_id_list = []
    new_all_db_students = []
    all_db_students = get_class_students(db=db, class_room_id=class_room_id)
    
    if all_db_students == []:
        student_db = Students(**new_student_data.dict(), roll_number=1)
        db.add(student_db)
        db.commit()
        db.refresh(student_db)
        return student_db
    else:
        for i in all_db_students:
            student_name_list.append(i.name)
            student_id_list.append(i.id)
            student_dict = dict(i)
            new_all_db_students.append(student_dict)

        student_db = new_student_data.dict(exclude_unset=True)
        student_db['id'] = max(student_id_list)+1
        new_all_db_students.append(student_db)
        new_all_db_students = sorted(new_all_db_students, key=lambda d: d['name'])

        for i in range(1,len(new_all_db_students)):
            new_all_db_students[i-1]['roll_number'] = i
            if new_all_db_students[i-1]['id'] == student_db['id']:
                student_db['roll_number'] = i

            print(new_all_db_students[i-1]['id'],'=-0987654321234567890-')
            student = db.get(Students, new_all_db_students[i-1]['id'])
            for key, value in new_all_db_students[i-1].items():
                setattr(student, key, value)
            db.add(student)
            db.commit()
            db.refresh(student)
        return student_db

        # student_name_list.append(student_name)
        # sorted(student_name_list)
        # for i in range(1,len(student_name_list)-1):
        #     if flag:
        #         if student_name_list[i] == student_name:
        #             print('=1=1=1=1=1=1=1=1==1=1=1=1==1=1')
        #             append_student_data = Students(**student_data.dict(), roll_number=i)
        #             flag = False
        #     else:
        #         # print(all_db_students[i],'````````````````````````````````````````````````')
        #         all_db_students[i].roll_number = i
        #         print(all_db_students, 'after ============================')

        # all_db_students.append(append_student_data)
        # for db_student in all_db_students:
        #     student = Students()
        #     student_db = db_student.dict(exclude_unset=True)
        #     print(student_db,'------------------------------------+++++++++++++++++++++++++++++++++++')
        #     for key, value in student_db.items():
        #         setattr(student, key, value)
        #     db.add(student)
        #     db.commit()
        #     db.refresh(student)


def get_class_students(db, class_room_id):
    list_class_students = (db.query(Students).filter(
        Students.class_room == class_room_id).all())
    return list_class_students



def get_student(**kwargs):
    if "db" in kwargs:
        db = kwargs["db"]
        if "student_id" in kwargs:
            student_id = kwargs["student_id"]
            list_of_students = db.get(Students, student_id)

            if list_of_students:
                return list_of_students
            else:
                exception.Exception_id_not_found('student')

        if "limit" in kwargs and "skip" in kwargs:
            skip = kwargs["skip"]
            limit = kwargs["limit"]
            list_of_students = db.query(
                Students).offset(skip).limit(limit).all()
        else:
            list_of_students = db.query(Students).all()
        return list_of_students

    else:
        exception.Exception_database_error()
