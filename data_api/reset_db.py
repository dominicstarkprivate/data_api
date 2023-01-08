from data_api import database


def reset_db():
    database.init_db()
    return None


if __name__ == "__main__":
    reset_db()
