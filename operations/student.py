from fastapi import HTTPException, status, Depends,BackgroundTasks
from models.sql_models.students import Students
from sqlmodel import select
import exception
from models.pydantic_models.response.student import FinalStudentResponse
from models.pydantic_models.request.student import StudentLoginTokenDataRequest
from passlib.context import CryptContext
from configaration import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.database import get_db
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/student/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, user: str):
    user = db.query(Students).where(Students.email == user).all()
    if user:
        user_dict = vars(user[0])
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
        print(
            payload,
            "---------------------------------------------------------------------------------------",
        )
        email: str = payload.get("sub")
        if email is None:
            exception.HTTP_401_UNAUTHORIZED("Could not validate credentials")
        token_data = StudentLoginTokenDataRequest(email=email)
    except JWTError:
        exception.HTTP_401_UNAUTHORIZED("Could not validate credentials")
    user = get_user(db, user=token_data.email)
    if user is None:
        exception.HTTP_401_UNAUTHORIZED("Could not validate credentials")
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
    list_students = get_student(db=db)
    list_students = sorted(list_students, key=lambda d: d.id)
    length = len(list_students)
    if all_db_students == []:
        student_db = Students(**new_student_data.dict(), roll_number=1)
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
                student_db = Students(**student_db)
                db.add(student_db)
                db.commit()
                db.refresh(student_db)

            id = new_all_db_students[i - 1]["id"]
            student = db.get(Students, id)
            for key, value in new_all_db_students[i - 1].items():
                print("Key :", key, "value :", value)
                setattr(student, key, value)
            db.add(student)
            db.commit()
        db.refresh(student)
        return returnvalue


def get_class_students(db, class_room_id):
    list_class_students = (
        db.query(Students).filter(Students.class_room == class_room_id).all()
    )
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
                exception.Exception_id_not_found("student")

        if "class_room_id" in kwargs:
            class_room_id = kwargs["class_room_id"]
            list_of_students = (
                db.query(Students).filter(Students.class_room == class_room_id).all()
            )
            if list_of_students:
                return list_of_students
            else:
                exception.Exception_students_null()

        if "student_roll_number" in kwargs:
            student_roll_number = kwargs["student_roll_number"]
            list_of_students = (
                db.query(Students)
                .filter(Students.roll_number == student_roll_number)
                .first()
            )
            if list_of_students:
                return list_of_students
            else:
                exception.Exception_id_not_found("Roll number")

        if "limit" in kwargs and "skip" in kwargs:
            skip = kwargs["skip"]
            limit = kwargs["limit"]
            list_of_students = db.query(Students).offset(skip).limit(limit).all()
        else:
            list_of_students = db.query(Students).all()
        return list_of_students
    else:
        exception.Exception_database_error()
