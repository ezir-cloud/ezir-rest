from sqlalchemy import create_engine , Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

import requests
import calendar
import datetime
import datetime as dt
import json
from apscheduler.schedulers.blocking import BlockingScheduler


Engine = create_engine('sqlite:///github_repo_job_details.sqlite')
Base = declarative_base()
Session_macker = sessionmaker( bind= Engine)
session = Session_macker()

# JobId, JobType,CreatedAt, UpdatedAt, JobObject, Jobstatus, Joblog, previousjobid.
class githubrepoapi(Base):
    __tablename__ = 'githubrepoapi'
    JobId          = Column(String(200))
    JobType        = Column(String(200))
    CreatedAt      = Column(String(200))
    UpdatedAt      = Column(String(200))
    JobObject      = Column(String(200), primary_key=True)
    Jobstatus      = Column(String(200))
    Joblog         = Column(String(200))
    previousjobid  = Column(String(200))

# Base.metadata.create_all(Engine)



sched = BlockingScheduler()

class GitRepoApisDetails:

        def job_is_get_repo(self,query_url):



            headers = {'content-type': 'application/json'}
            self.response = requests.get(query_url, headers=headers)
            self.matched_repositories = self.response.json()

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
            print(all_repositories_details)
            return all_repositories_details


        def get_repo_details_by_month(self,repo_name,year,month):

            total_days=calendar.monthrange(year,month)[1]
            self.total_urls = []



            for days in range(1,total_days+1):

                day_obj = datetime.date(year, month, days)
                self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                self.total_urls.append(self.target_url)
            self.add_job_for_githubapi(self.total_urls)


        def get_repo_details_by_year(self, repo_name, year):

            self.total_urls = []
            for month in range(1, 13):

                total_days=calendar.monthrange(year,month)[1]
                for days in range(1,total_days+1):

                    day_obj = datetime.date(year, month, days)
                    self.target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=repo_name,date=day_obj)
                    self.total_urls.append(self.target_url)
            self.add_job_for_githubapi(self.total_urls)


        def add_job_for_githubapi(self, year, month, day, hour, mint, sec):

            job_run_data_time =dt.timedelta(seconds=20)
            print(job_run_data_time)
            # job_date_time_increase = job_run_data_time + job_run_data_time
            # print(job_date_time_increase)
            datetime_as_integer = job_run_data_time + 20
            print(datetime_as_integer)
            create_datatime = datetime.datetime(year, month, day, hour, mint, sec) +job_run_data_time
            print(create_datatime)

            flag = 1
            # for url in range(1, 31):


                # if flag == 1:
                    # print("if")

                    # new_datatime = create_datatime
                    # print(new_datatime)
                    # sched.add_job(obj.job_is_get_repo, 'date', run_date=create_datatime,  misfire_grace_time=50 ,args=[url])
                    # flag = 0
                # else:
                    # print(flag)
                    # print(new_datatime)
                    # print("else")
                    #
                    # new_datatime = create_datatime + dt.timedelta(seconds=40)
                    # update_datatime = new_datatime
                    # print(new_datatime)
                    # return_job_obj=sched.add_job(obj.job_is_get_repo, 'date', run_date=create_datatime,  misfire_grace_time=50, args=[url])
obj=GitRepoApisDetails()
# url=obj.get_repo_details_by_month("dockerfile",2020,2)
job_by_date = obj.add_job_for_githubapi(2020, 7, 31, 22, 4, 00)
try:
    sched.start()
except (Exception):
    pass
