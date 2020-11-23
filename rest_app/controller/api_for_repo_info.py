# from _operator import index
from githubapis.search import GitRepositoryApisDetails
from rest_app.dal.dal import insert_api_repo_info,get_api_repo_info


def api_for_repo_details(reponame):
    github_api_repo_details = GitRepositoryApisDetails()
    repo_info = github_api_repo_details.search_repository_details(reponame)
    return repo_info


def insert_repo_details(api_repo_info):

    index='github_repo_details'
    insert_api_repo_info(index,api_repo_info)


def get_repo_details(repo_name):

    index = 'github_repo_details'
    repoinfo= get_api_repo_info(index,repo_name)
    return repoinfo







