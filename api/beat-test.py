from datetime import datetime, timedelta
import pytz
import shelve

now = datetime.now(tz=pytz.utc)
file_data = shelve.open('celerybeat-schedule') # Name of the file used by PersistentScheduler to store the last run times of periodic tasks. 
print(now)
for task_name, task in file_data['entries'].items():
    print(task_name, task.last_run_at)
#    try:
#        assert now  < task.last_run_at + task.schedule.run_every
#    except AttributeError:
#        assert timedelta() < task.schedule.remaining_estimate(task.last_run_at)

