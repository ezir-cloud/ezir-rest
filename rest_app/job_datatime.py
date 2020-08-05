import calendar
import datetime
import datetime as dt
import json
import uuid
import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from requests.exceptions import ConnectionError
from sqlalchemy import desc


sched = BlockingScheduler()

Engine = create_engine('sqlite:///github_repo_job_details.sqlite')
Base = declarative_base()
Session_macker = sessionmaker( bind= Engine)
session = Session_macker()

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

Base.metadata.create_all(Engine)

class GitRepoApisDetails:

    def job_is_get_repo(self,query_url, job_id):
        print(query_url)
        print(job_id)

        try:

            headers = {'content-type': 'application/json'}
            self.response = requests.get(query_url, headers=headers)
            self.matched_repositories = self.response.json()
            self.total_count= self.matched_repositories.get('total_count')
            print(self.total_count)

            if self.total_count==0:
                session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
                    {job_details_by_githubapi.Jobstatus:'completed', job_details_by_githubapi.Joblog:str (self.matched_repositories)},
                    synchronize_session=False)
                session.commit()

            else:
                session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
                    {job_details_by_githubapi.Jobstatus:'completed', job_details_by_githubapi.Joblog:'get repository details'},
                    synchronize_session=False)
                session.commit()

                all_repositories_details = []
                for repo in self.matched_repositories["items"]:

                    repo_details = dict()
                    repo_details["id"] = repo.get("id")
                    repo_details["name"] = repo.get("name")
                    repo_details["full_name"] = repo.get("full_name")
                    repo_details["private"] = repo.get("private")
                    repo_details["owner"] = dict()
                    repo_details["owner"]["login"] = repo.get("owner").get("login")
                    repo_details["owner"]["id"] = repo.get("owner").get("id")
                    repo_details["owner"]["html_url"] = repo.get("owner").get("html_url")
                    repo_details["html_url"] = repo.get("html_url")
                    repo_details["description"] = repo.get("description")
                    repo_details["url"] = repo.get("url")
                    repo_details["contents_url"] = repo.get("contents_url")
                    repo_details["created_at"] = repo.get("created_at")
                    repo_details["updated_at"] = repo.get("updated_at")

                    if repo.get("license"):
                        repo_details["license"] = dict()
                        repo_details["license"]["key"] = repo.get("key")
                        repo_details["license"]["name"] = repo.get("name")
                        repo_details["license"]["spdx_id"] = repo.get("spdx_id")
                        repo_details["license"]["url"] = repo.get("url")

                    repo_details["forks"] = repo.get("forks")
                    repo_details["watchers"] = repo.get("watchers")
                    all_repositories_details.append(repo_details)



        except ConnectionError as exception_msg:

            session.query(job_details_by_githubapi).filter(job_details_by_githubapi.JobId == job_id).update(
                {job_details_by_githubapi.Jobstatus: 'not_completed',
                 job_details_by_githubapi.Joblog: str(exception_msg)}, synchronize_session=False)
            session.commit()
            self.re_add_fail_jobs(query_url, job_id)


    def get_repo_details_by_month(self,file_name, file_created_year, file_created_month,  job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):


        current_time = dt.datetime.now()
        change_current_time_format = dt.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")
        job_run_time = dt.datetime(job_year, job_month, job_day, job_hr, job_min, job_sec)
        change_job_run_time_format = dt.datetime.strftime(job_run_time, "%Y-%m-%d %H:%M:%S")

        if change_current_time_format > change_job_run_time_format:
            print("please enter valid datetime to set job runtime")

        else:
            total_days=calendar.monthrange(file_created_year,file_created_month)[1]
            nextTime = None
            for days in range(1,total_days+1):

                day_obj = datetime.date(file_created_year, file_created_month, days)
                target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=file_name,date=day_obj)

                uid = uuid.uuid4().hex
                if nextTime is None:
                    job_run_time = dt.datetime(job_year, job_month, job_day, job_hr, job_min, job_sec)
                    nextTime =job_run_time + dt.timedelta(seconds=job_interval_count)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    self.add_job_by_time(target_url,  run_date, uid)

                else:
                    nextTime = nextTime + dt.timedelta(seconds=job_interval_count)
                    run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                    self.add_job_by_time(target_url,  run_date, uid)

    def add_job_by_time(self, target_url, run_date, uid):

        sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=10, args=[target_url, uid], id=uid)

        job_details = {}
        for job in sched.get_jobs():
            job_details['name'] = "%s" % job.name
            job_details['trigger'] = "%s" % job.trigger
        job_details_json = json.dumps(job_details)

        github_repo_api = job_details_by_githubapi(JobId=uid, JobType='github', CreatedAt=run_date,
                                                   UpdatedAt='', JobObject=job_details_json,
                                                   Jobstatus='pending', Joblog='job log', previousjobid='0')
        session.add(github_repo_api)
        session.commit()

    def re_add_fail_jobs(self, job_id, query_url ):

        print(job_id)
        print(query_url)
        select_job_details = session.query(job_details_by_githubapi).order_by(desc(job_details_by_githubapi.CreatedAt))
        select_one_job = select_job_details.first()
        last_job_datetime = select_one_job.CreatedAt
        print(last_job_datetime)


obj=GitRepoApisDetails()
# (file_name, file_created_year, file_created_month,job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):
obj.get_repo_details_by_month("dockerfile", 2020, 4, 2020, 8, 5, 18, 11, 10, 6)

sched.start()