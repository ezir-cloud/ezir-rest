from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo= True)

engine.execute('CREATE TABLE "EX1" ('
                                    'id INTEGER NOT NULL ,'
                                    'name VARCHAR,'
                                    'PRIMARY KEY (id));')
engine.table_names()
