from sqlalchemy import create_engine, MetaData, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'users_emails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String, nullable=False)
    Name = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Template = Column(String, nullable=False)

class Database:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///mails.sqlite', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def save_new_email(self, id: str, name: str, email: str, template: str):
        session = self.Session()
        try:
            new_email_data = UserData(
                UserId=id,
                Name=name,
                Email=email,
                Template=template
            )
            session.add(new_email_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_emails_by_user_id(self, user_id: str):
        session = self.Session()
        try:
            results = session.query(UserData).filter(UserData.UserId == user_id).all()
            return results
        finally:
            session.close()

if __name__ == "__main__":
    database = Database()
    database.save_new_email(id='1', name='aalu', email='mail', template='hello')
    # Retrieve data for user with user_id '1'
    user_emails = database.get_emails_by_user_id(user_id='1')
    for email in user_emails:
        print(f"Name: {email.Name}, Email: {email.Email}, Template: {email.Template}")