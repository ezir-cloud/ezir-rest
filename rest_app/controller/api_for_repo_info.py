from _operator import index
from githubapis.search import GitRepositoryApisDetails
from rest_app.dal.dal import insert_api_repo_info


def api_for_repo_details(reponame):
    github_api_repo_details = GitRepositoryApisDetails()
    repo_info = github_api_repo_details.search_repository_details(reponame)
    return repo_info


def insert_repo_details(api_repo_info):

    index='github_repo_details'
    repo_info = insert_api_repo_info(api_repo_info,index)
    return repo_info