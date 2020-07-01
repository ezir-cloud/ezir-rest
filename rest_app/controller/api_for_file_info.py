from _operator import index
from githubapis.search import GithubRepoApis
from rest_app.dal.dal import insert_api_file_info, search_file_by_name


def api_for_file_details(reponame,filename):
    github_api_files_details = GithubRepoApis()
    file_info = github_api_files_details.get_matched_files_in_repo_by_file_name(reponame,filename)
    return file_info


def insert_file_details(api_file_info):
    index='github_file_details'
    file_info = insert_api_file_info(api_file_info,index)
    return file_info


def search_file_details(file_name):
    index='github_file_details'
    search_file_name = search_file_by_name(index,file_name)
    return search_file_name