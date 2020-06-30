from _operator import index
from githubapis.search import GithubRepoApis
from rest_app.dal.dal import insert_api_file_info


def api_for_file_details(reponame,filename):
    github_api_files_details = GithubRepoApis()
    file_info = github_api_files_details.get_matched_files_in_repo_by_file_name(reponame,filename)
    return file_info


def insert_file_details(api_file_info):
    index='github_file_details'
    file_info = insert_api_file_info(api_file_info,index)
    return file_info