from flask import Flask, jsonify, request
from githubapis.search import GitRepositoryApisDetails
from githubapis.search import Github
from rest_app.controller.api_for_repo_info import api_for_repo_details, insert_repo_details

app = Flask(__name__)

@app.route('/repo-details', methods=['POST'])
def repo_details():
    reponame = request.args.get('reponame')

    repo_details = api_for_repo_details(reponame)
    api_repo_info = insert_repo_details(repo_details)
    return jsonify(api_repo_info)

if __name__ == '__main__':
    app.run (debug = True)
