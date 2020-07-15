from rest_app.dal import githubrepoapi_db

def githubrepo():

    dbms = githubrepoapi_db.Githubrepodb(githubrepoapi_db.SQLITE, dbname='githubrepoapi.sqlite')

    dbms.create_db_tables()

if __name__ == "__main__":
    githubrepo()
