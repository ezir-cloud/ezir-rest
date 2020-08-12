from flask import Flask, jsonify, request
from rest_app.controller.api_for_repo_info import api_for_repo_details, insert_repo_details,get_repo_details

app = Flask(__name__)

@app.route('/repo-details', methods=['POST'])
def repo_details():

    reponame = request.args.get('reponame')
    repo_details = api_for_repo_details(reponame)
    insert_repo_details(repo_details)


@app.route('/fatch-repo-details/<repo_name>', methods=['GET'])
def fetch_repo_details(repo_name):

    details=get_repo_details(repo_name)
    return jsonify(details)


if __name__ == '__main__':
    app.run (debug = True)


