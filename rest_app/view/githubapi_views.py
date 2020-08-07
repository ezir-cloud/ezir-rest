from  elasticsearch import Elasticsearch
from flask import Flask, jsonify, request

from rest_app.controller.api_for_repo_info import api_for_repo_details_by_month, api_for_repo_details_by_year, \
    api_for_repo_details_by_two_date, api_for_repo_details_by_date, insert_repo_details, search_repo_details

app = Flask(__name__)
es = Elasticsearch()

@app.route('repositories_details_by_month', Method=['GET'])
def repo_details_by_month():
    repo_name = request.args.get('repo_name')
    repo_created_year = request.args.get('repo_created_year')
    repo_created_month = request.args.get('repo_created_month')
    repo_details = api_for_repo_details_by_month(repo_name, repo_created_year, repo_created_month)
    repositories_info = insert_repo_details(repo_details)
    return jsonify(repositories_info)


@app.route('repositories_details_by_year', Method=['GET'])
def repo_details_by_year():
    repo_name = request.args.get('repo_name')
    repo_created_year = request.args.get('repo_created_year')
    repo_details = api_for_repo_details_by_year(repo_name, repo_created_year)
    repositories_info = insert_repo_details(repo_details)
    return jsonify(repositories_info)


@app.route('repositories_details_by_two_date', Method=['GET'])
def repo_details_by_two_date():
    repo_name = request.args.get('repo_name')
    repo_created_year1 = request.args.get('repo_created_year1')
    repo_created_month1 = request.args.get('repo_created_month1')
    repo_created_day1 = request.args.get('repo_created_day1')
    repo_created_year2 = request.args.get('repo_created_year2')
    repo_created_month2 = request.args.get('repo_created_month2')
    repo_created_day2 = request.args.get('repo_created_day2')
    repo_details = api_for_repo_details_by_two_date(repo_name, repo_created_year1, repo_created_month1, repo_created_day1,
                                                    repo_created_year2, repo_created_month2, repo_created_day2)
    repositories_info = insert_repo_details(repo_details)
    return jsonify(repositories_info)

@app.route('repository_details_by_date', Method=['GET'])
def repo_details_by_date():
    repo_name = request.args.get('repo_name')
    repo_created_year = request.args.get('repo_created_year')
    repo_created_month = request.args.get('repo_created_month')
    repo_created_day = request.args.get('repo_created_day')
    repo_details = api_for_repo_details_by_date(repo_name, repo_created_year, repo_created_month, repo_created_day)
    repositories_info = insert_repo_details(repo_details)
    return jsonify(repositories_info)

@app.route('/fetch_repo_info/<repo_name>', methods=['GET'])
def fetch_repo_info(repo_name):
    repo_name =search_repo_details(repo_name)
    return jsonify(repo_name)

if __name__ == '__main__':
    app.run (debug = True)