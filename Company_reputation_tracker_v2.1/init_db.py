from database.db_utils import init_db, get_db_session
from database.schema import Company

def main():
    init_db()
    session = get_db_session()
    if not session.query(Company).first():
        tesla = Company(name="Tesla", aliases="TSLA, Tesla Inc")
        session.add(tesla)
        session.commit()
        print("Added example company: Tesla")
    session.close()

if __name__ == "__main__":
    main()
