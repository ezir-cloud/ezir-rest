from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from requests.exceptions import ConnectionError

import requests
import calendar
import datetime
import datetime as dt
import json
import uuid
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

Engine = create_engine('sqlite:///github_repo_job_details.sqlite')
Base = declarative_base()
Session_macker = sessionmaker( bind= Engine)
session = Session_macker()

# JobId, JobType,CreatedAt, UpdatedAt, JobObject, Jobstatus, Joblog, previousjobid.

class job_details_by_githubapi(Base):
    __tablename__ = 'job_details_by_githubapi'
    JobId          = Column(String(200),  primary_key=True)
    JobType        = Column(String(200))
    CreatedAt      = Column(String(200))
    UpdatedAt      = Column(String(200))
    JobObject      = Column(String(200))
    Jobstatus      = Column(String(200))
    Joblog         = Column(String(500))
    previousjobid  = Column(String(200))

# Base.metadata.create_all(Engine)


sched = BlockingScheduler()

class GitRepoApisDetails:


        def job_is_get_repo(self, query_url):
            print("url outside try block",query_url)
            # print("job id outside try block", job_id)
            # try:
            #
            #     headers = {'content-type': 'application/json'}
            #     self.response = requests.get(query_url, headers=headers)
            #     self.matched_repositories = self.response.json()
            #     print(self.matched_repositories['total_count'])
            #
            #     if self.matched_repositories['total_count']==0:
            #         session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
            #             {job_details_by_githubapi.Jobstatus:'completed', job_details_by_githubapi.Joblog:str (self.matched_repositories)},
            #             synchronize_session=False)
            #         session.commit()
            #
            #     else:
            #         session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
            #             {job_details_by_githubapi.Jobstatus:'completed', job_details_by_githubapi.Joblog:'get repository details'},
            #             synchronize_session=False)
            #         session.commit()
            #
            #         all_repositories_details = []
            #         for repo in self.matched_repositories["items"]:
            #
            #             repo_details = dict()
            #             repo_details["id"] = repo.get("id")
            #             repo_details["name"] = repo.get("name")
            #             repo_details["full_name"] = repo.get("full_name")
            #             repo_details["private"] = repo.get("private")
            #             repo_details["owner"] = dict()
            #             repo_details["owner"]["login"] = repo.get("owner").get("login")
            #             repo_details["owner"]["id"] = repo.get("owner").get("id")
            #             repo_details["owner"]["html_url"] = repo.get("owner").get("html_url")
            #             repo_details["html_url"] = repo.get("html_url")
            #             repo_details["description"] = repo.get("description")
            #             repo_details["url"] = repo.get("url")
            #             repo_details["contents_url"] = repo.get("contents_url")
            #             repo_details["created_at"] = repo.get("created_at")
            #             repo_details["updated_at"] = repo.get("updated_at")
            #
            #             if repo.get("license"):
            #                 repo_details["license"] = dict()
            #                 repo_details["license"]["key"] = repo.get("key")
            #                 repo_details["license"]["name"] = repo.get("name")
            #                 repo_details["license"]["spdx_id"] = repo.get("spdx_id")
            #                 repo_details["license"]["url"] = repo.get("url")
            #
            #             repo_details["forks"] = repo.get("forks")
            #             repo_details["watchers"] = repo.get("watchers")
            #             all_repositories_details.append(repo_details)
            #
            #         return all_repositories_details


            # except ConnectionError as exception_msg:
            #
            #     session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
            #         {job_details_by_githubapi.Jobstatus: 'not_completed',
            #          job_details_by_githubapi.Joblog: str(exception_msg)}, synchronize_session=False)
            #     session.commit()

                # self.retry_fail_jobs(job_id)


        def get_repo_details_by_month(self, repo_name, year_for_repo, month_for_repo, day_for_repo, year, month, day, hour, min, sec):

            # repo_by_date=dt.datetime(year_for_repo, month_for_repo, day_for_repo)
            # change_repo_by_date_format = dt.datetime.strftime(repo_by_date, "%Y-%m-%d %H:%M:%S")
            # docker_relase_date=dt.datetime(2013 , 12 , 21)
            # change_docker_relase_date_format = dt.datetime.strftime(docker_relase_date, "%Y-%m-%d %H:%M:%S")
            # current_datetime=dt.datetime.now()
            # change_current_date_format = dt.datetime.strftime(current_datetime, "%Y-%m-%d %H:%M:%S")
            #
            # if change_repo_by_date_format < change_docker_relase_date_format:
            #     print("The first public beta version of Docker Compose (version 0.0.1) was released on December 21,"
            #           " 2013.So please enter valid date")
            #
            # elif change_repo_by_date_format > change_current_date_format:
            #     print('you cant get future dockerfile details')
            #
            # else:
            #
            #     current_time = dt.datetime.now()
            #     job_run_time = dt.datetime(year, month, day, hour, min,sec)
            #     change_current_time_format = dt.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")
            #     change_job_run_time_format = dt.datetime.strftime(job_run_time, "%Y-%m-%d %H:%M:%S")
            #
            #     if change_current_time_format > change_job_run_time_format:
            #         print("please enter valid datetime to set job runtime")
            #
            #     else:

                    total_days=calendar.monthrange(year_for_repo, month_for_repo)[1]
                    self.total_urls = []

                    for day in range(day_for_repo, total_days+1):

                        day_obj = datetime.date(year_for_repo, month_for_repo, day)
                        self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                        self.total_urls.append(self.target_url)
                    print(self.total_urls)

                    job_datetime = datetime.datetime(year, month, day, hour, min, sec)
                    print(job_datetime)
                    self.add_job_for_githubapi(self.total_urls, job_datetime)


        def add_job_for_githubapi(self,total_urls,job_datetime):
            print(job_datetime)

            flag = 1
            nextTime = ''

            for url in total_urls:

                uid = uuid.uuid4().hex

                if flag == 1:

                    nextTime = job_datetime + dt.timedelta(seconds=10)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    print(run_date)
                    # sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=50, args=[url])
                    # print(' if url pass')

                    # job_object_details = {}
                    # for job in sched.get_jobs():
                    #
                    #     job_object_details['name'] = "%s" % job.name
                    #     job_object_details['trigger'] = "%s" % job.trigger
                    #
                    # job_details_json = json.dumps(job_object_details)
                    #
                    # github_repo_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=nextTime, UpdatedAt='6-08-20',
                    #                                       JobObject= job_details_json, Jobstatus='pending',
                    #                                       Joblog='job log', previousjobid='0')
                    # session.add(github_repo_api)
                    # session.commit()


                    flag = 0

                else:

                    nextTime = nextTime + dt.timedelta(seconds=10)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    print(run_date)
                    sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=50, args=[url])
                    print('else url pass')
                    job_details = {}

                    for job in sched.get_jobs():
                        job_details['name'] = "%s" % job.name
                        job_details['trigger'] = "%s" % job.trigger

                    job_details_json = json.dumps(job_details)
                    github_repo_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=nextTime,
                                                          UpdatedAt='6-08-20', JobObject=job_details_json,
                                                          Jobstatus='pending', Joblog='job log', previousjobid='0')
                    session.add(github_repo_api)
                    session.commit()




obj=GitRepoApisDetails()
url=obj.get_repo_details_by_month("dockerfile",2020,7,29,2020,8,5,9,56,45)


try:
    sched.start()
except (Exception):
    pass