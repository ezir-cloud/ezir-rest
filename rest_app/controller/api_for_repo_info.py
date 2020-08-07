from rest_app.dal.dal_githubrepo import insert_api_repo_info, search_repo_by_name
from rest_app.githubrepo_details import GitRepoApisDetails


def api_for_repo_details_by_month(repo_name, repo_created_year, repo_created_month):
    github_api_repo_details = GitRepoApisDetails()
    repo_info = github_api_repo_details.get_repo_details_by_month(repo_name, repo_created_year, repo_created_month)
    return repo_info


def api_for_repo_details_by_year(repo_name, repo_created_year):
    github_api_repo_details = GitRepoApisDetails()
    repo_info = github_api_repo_details.get_repo_details_by_year(repo_name, repo_created_year)
    return repo_info


def api_for_repo_details_by_two_date(repo_name, repo_created_year1, repo_created_month1, repo_created_day1,
                                                    repo_created_year2, repo_created_month2, repo_created_day2):
    github_api_repo_details = GitRepoApisDetails()
    repo_info = github_api_repo_details.get_repo_details_by_two_date(repo_name, repo_created_year1, repo_created_month1, repo_created_day1,
                                                    repo_created_year2, repo_created_month2, repo_created_day2)
    return repo_info

def api_for_repo_details_by_date(repo_name, repo_created_year, repo_created_month, repo_created_day):
    github_api_repo_details = GitRepoApisDetails()
    repo_info = github_api_repo_details.get_repo_by_date(repo_name, repo_created_year, repo_created_month, repo_created_day)
    return repo_info

def insert_repo_details(repo_info):
    index='github_file_details'
    file_info = insert_api_repo_info(repo_info,index)
    return file_info


def search_repo_details(repo_name):
    index='github_file_details'
    search_repo_name = search_repo_by_name(index,repo_name)
    return search_repo_name