from add_job_running_scheduler.scheduler_start import scheduler

print("add_jobs: ", id(scheduler))
print(scheduler.state)

def say_hello_job():
    print ("Hello1")

job_obj=scheduler.add_job(say_hello_job, 'interval', seconds=10)
print(job_obj.id)
scheduler.start()
