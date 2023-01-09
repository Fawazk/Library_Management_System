from fastapi import HTTPException, status, Depends, BackgroundTasks
from models.sql_models.account import Account
from sqlmodel import select
import exception
from models.pydantic_models.response.account import (
    FinalStudentResponse,
    FinalStaffResponse,
    ListStudentResponse,
    ListStaffResponse,
)
from models.pydantic_models.request.account import StudentLoginTokenDataRequest
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.database import get_db
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from models.pydantic_models.settings import settings

token_settings = settings()
ACCESS_TOKEN_EXPIRE_MINUTES = token_settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = token_settings.ALGORITHM
SECRET_KEY = token_settings.SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/account/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, user: str):
    user = db.query(Account).where(Account.email == user).all()
    if user:
        user_dict = vars(user[0])
        if user_dict["is_staff_user"] == True:
            return FinalStaffResponse(**user_dict)
        return FinalStudentResponse(**user_dict)
    else:
        return {}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db, user: str, password: str):
    user = get_user(db, user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            exception.HTTP_401_UNAUTHORIZED("Not a validate credentials")
        token_data = StudentLoginTokenDataRequest(email=email)
    except JWTError:
        exception.HTTP_401_UNAUTHORIZED("Not a validate credentials")
    user = get_user(db, user=token_data.email)
    if user is None:
        exception.HTTP_401_UNAUTHORIZED("Not a validate credentials")
    return user


async def get_current_active_user(
    current_user: FinalStudentResponse = Depends(get_current_user),
):
    if current_user:
        if current_user.is_active:
            return current_user
        else:
            raise HTTPException(status_code=400, detail="Inactive user")
    else:
        raise HTTPException(status_code=400, detail="User is None pls login")


async def get_current_active_staff_user(
    current_user: FinalStaffResponse = Depends(get_current_user),
):
    if current_user:
        if current_user.is_active and current_user.is_staff_user:
            return current_user
        else:
            raise HTTPException(status_code=400, detail="Inactive user")
    else:
        raise HTTPException(status_code=400, detail="User is None pls login")


def login_school(db, form_data):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        exception.HTTP_401_UNAUTHORIZED("Incorrect user or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def register_student(db, new_student_data):
    password = get_password_hash(new_student_data.password)
    new_student_data.password = password
    class_room_id = new_student_data.class_room
    flag = True
    student_name_list = []
    new_all_db_students = []
    all_db_students = get_class_students(db=db, class_room_id=class_room_id)
    list_students = get_account(db=db)
    list_students = sorted(list_students, key=lambda d: d.id)
    length = len(list_students)
    if all_db_students == []:
        student_db = Account(**new_student_data.dict(), roll_number=1)
        db.add(student_db)
        db.commit()
        db.refresh(student_db)
        return student_db
    else:
        for i in all_db_students:
            student_name_list.append(i.name)
            student_dict = dict(i)
            new_all_db_students.append(student_dict)

        student_db = new_student_data.dict(exclude_unset=True)
        student_db["id"] = list_students[length - 1].id + 1
        new_all_db_students.append(student_db)
        new_all_db_students = sorted(new_all_db_students, key=lambda d: d["name"])

        for i in range(1, len(new_all_db_students) + 1):
            new_all_db_students[i - 1]["roll_number"] = i
            if flag and new_all_db_students[i - 1]["id"] == student_db["id"]:
                flag = False
                student_db["roll_number"] = i
                returnvalue = student_db
                student_db = Account(**student_db)
                db.add(student_db)
                db.commit()
                db.refresh(student_db)

            id = new_all_db_students[i - 1]["id"]
            student = db.get(Account, id)
            for key, value in new_all_db_students[i - 1].items():
                setattr(student, key, value)
            db.add(student)
            db.commit()
        db.refresh(student)
        return returnvalue


def register_staff(db, staff_data):
    password = get_password_hash(staff_data.password)
    staff_data.password = password
    staff_data_db = Account(**staff_data.dict(), is_staff_user=True)
    db.add(staff_data_db)
    db.commit()
    db.refresh(staff_data_db)
    return staff_data_db


def get_class_students(db, class_room_id):
    list_class_students = (
        db.query(Account).filter(Account.class_room == class_room_id).all()
    )
    return list_class_students


def get_account(db, params: Dict = None):
    if db:
        if params:
            if "student_id" in params and params["student_id"] != None:
                student_id = params["student_id"]
                list_of_students = (
                    db.query(Account)
                    .filter(Account.id == student_id)
                    .filter(Account.is_staff_user == False)
                    .first()
                )
                if list_of_students:
                    return list_of_students
                else:
                    exception.Exception_id_not_found("student")

            if "staff_id" in params and params["staff_id"] != None:
                staff_id = params["staff_id"]
                list_of_students = (
                    db.query(Account)
                    .filter(Account.id == staff_id)
                    .filter(Account.is_staff_user == True)
                    .first()
                )
                if list_of_students:
                    return list_of_students
                else:
                    exception.Exception_id_not_found("staff")

            if "class_room_id" in params and params["class_room_id"] != None:
                class_room_id = params["class_room_id"]
                list_of_students = (
                    db.query(Account).filter(Account.class_room == class_room_id).all()
                )
                if list_of_students:
                    return list_of_students
                else:
                    exception.Exception_students_null()

            if "roll_number" in params and params["roll_number"] != None:
                roll_number = params["roll_number"]
                list_of_students = (
                    db.query(Account).filter(Account.roll_number == roll_number).first()
                )
                if list_of_students:
                    return list_of_students
                else:
                    exception.Exception_id_not_found("roll number")

            if "list_student" in params and params["list_student"] == True:
                list_of_students = (
                    db.query(Account).filter(Account.is_staff_user == False).all()
                )
                new_list_of_students = []
                for data in list_of_students:
                    new_list_of_students.append(ListStudentResponse(**data.dict()))
                return new_list_of_students

            if "list_staff" in params and params["list_staff"] == True:
                list_of_students = (
                    db.query(Account).filter(Account.is_staff_user == True).all()
                )
                new_list_of_students = []
                for data in list_of_students:
                    new_list_of_students.append(ListStaffResponse(**data.dict()))
                return new_list_of_students

            if "limit" in params and "skip" in params:
                skip = params["skip"]
                limit = params["limit"]
                list_of_students = db.query(Account).offset(skip).limit(limit).all()
                return list_of_students
        else:
            list_of_students = []
            list_of_students = db.query(Account).all()
            return list_of_students
    else:
        exception.Exception_database_error()
