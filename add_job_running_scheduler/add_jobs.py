from add_job_running_scheduler.scheduler_start import scheduler

print("scheduler state: ", scheduler.state)
def say_hello_job():
    print ("Hello")


job_obj=scheduler.add_job(say_hello_job, 'interval', seconds=3)
print(job_obj)
print(job_obj.id)

jobs = scheduler.get_jobs()
print(jobs)

