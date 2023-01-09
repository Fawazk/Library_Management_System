from sqlmodel import create_engine, Session

postgresql_file_name = "library_management_system2"
postgresql_url = (
    f"postgresql://postgres:postgres@172.17.0.1:5433/{postgresql_file_name}"
    # f"postgresql://postgres:postgres@localhost:5432/{postgresql_file_name}"
)

connect_args = {"check_same_thread": False}
engine = create_engine(postgresql_url, echo=True)


def get_db():
    db = Session(engine)
    return db
