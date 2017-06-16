#!/bin/bash/python3

from crontab import CronTab
import datetime
import logging
import os


def set_execution(job_path, run_cmd, on_off, hour, minute):
    '''(str, str, int, int) -> None
    Adds file/job (cmd) at the job_path to user path to run daily on hour and
    minute given. Will enable automatic updating based on bool value of on_off.
    '''
    # getting the user cron job table
    user_cron  = CronTab(user=True)
    if user_cron != None:
        cmd = os.path.join(job_path, run_cmd)
        # Remove existing cron entry:
        user_cron.remove_all(command=cmd)
        # Create new entry:
        job =  user_cron.new(command=cmd)
        # Set the hour (24 hours) and minutes (0-59) of job:
        job.hour.on(hour)
        job.minute.on(minute)
        job.enable(on_off)
        user_cron.write()
        return True
    else:
        logging.exception('%s: Failed to set the cron job',
                          str(datetime.datetime.now()))
        return False