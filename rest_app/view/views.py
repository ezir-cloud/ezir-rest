from flask import Flask, jsonify, request
from githubapis.search import GithubRepoApis
from githubapis.search import Github
from rest_app.controller.api_for_file_info import api_for_file_details, insert_file_details

app = Flask(__name__)


@app.route('/files-info', methods=['POST'])
def file_details():

    reponame = request.args.get('reponame')
    filename = request.args.get('filename')
    file_details = api_for_file_details(reponame,filename)
    api_file_info = insert_file_details(file_details)

    return jsonify(api_file_info)


if __name__ == '__main__':
    app.run (debug = True)