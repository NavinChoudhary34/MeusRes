
from meusres.database import Base, engine
from meusres import models


def init_database():
    Base.metadata.create_all(bind=engine)
    print("MeusRes database initialized successfully.")


if __name__ == "__main__":
    init_database()

