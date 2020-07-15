from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime

SQLITE  = 'sqlite'

GITHUBREPO  = 'githubrepo'

class Githubrepodb:

    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None


    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            print(engine_url)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        githubrepo = Table(GITHUBREPO, metadata,
                      Column('JobId', Integer, primary_key=True),
                      Column('JobType', String),
                      Column('CreatedAt', DateTime),
                      Column('UpdatedAt',DateTime),
                      Column('JobObject', String)
                      )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)
