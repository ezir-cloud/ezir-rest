import calendar
import datetime
import datetime as dt


from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

class GitRepoApisDetails:

    def job_is_get_repo(self,query_url):
        print(query_url)

    def get_repo_details_by_month(self,file_name, file_created_year, file_created_month,  job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):

        total_days=calendar.monthrange(file_created_year,file_created_month)[1]

        nextTime = None
        for days in range(1,total_days+1):

            day_obj = datetime.date(file_created_year, file_created_month, days)
            target_url = "https://api.github.com/search/repositories?q={repo_name}+created:{date}".format(repo_name=file_name,date=day_obj)

            if nextTime is None:
                job_run_time = dt.datetime(job_year, job_month, job_day, job_hr, job_min, job_sec)
                nextTime =job_run_time + dt.timedelta(seconds=job_interval_count)
                run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                self.add_job_by_time(target_url, nextTime, run_date)

            else:
                nextTime = nextTime + dt.timedelta(seconds=job_interval_count)
                run_date = dt.datetime.strftime(nextTime, "%Y-%m-%d %H:%M:%S")
                self.add_job_by_time(target_url, nextTime, run_date)

    def add_job_by_time(self, target_url, nextTime, run_date):

        if nextTime is None:
            print(run_date)
            sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=10, args=[target_url])
        else:
            print(run_date)
            sched.add_job(obj.job_is_get_repo, 'date', run_date=run_date, misfire_grace_time=10, args=[target_url])


obj=GitRepoApisDetails()
# (file_name, file_created_year, file_created_month,job_year, job_month, job_day, job_hr, job_min, job_sec,  job_interval_count):
obj.get_repo_details_by_month("dockerfile", 2020, 4, 2020, 8, 5, 13, 10, 10, 10)

sched.start()