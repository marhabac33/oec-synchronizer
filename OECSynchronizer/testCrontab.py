from oec_sync_utils import set_cron_job
from crontab import CronTab
import unittest, os

class TestCronTab(unittest.TestCase):

    def test_hour_crontab(self):
        set_execution = getattr(set_cron_job, 'set_execution')
        # test minutes
        cwd = os.getcwd()
        test_file = open('hour', 'w')
        test_file.close()
        command = "test " + cwd
        set_execution(command, 'hour', True, hour=0, minute=1)

        user_cron  = CronTab(user=True)
        for line in user_cron.lines:
            if 'hour' in line:
                self.assertEqual('0 1 * * * '+ os.path.dirname(os.path.abspath(test_file)), line, 'checking hour timing\t...failed')
                user_cron.remove_all('test')
        os.remove('hour')

    def test_min_crontab(self):
        set_execution = getattr(set_cron_job, 'set_execution')
        # test hours
        cwd = os.getcwd()
        test_file = open('minute', 'w')
        test_file.close()
        command = "test " + cwd
        set_execution(command, 'minute', True, hour=1, minute=0)

        user_cron  = CronTab(user=True)
        for line in user_cron.lines:
            if 'minute' in line:
                self.assertEqual('1 0 * * * '+os.path.dirname(os.path.abspath(test_file)), line, 'checking minute timing\t...failed')
                user_cron.remove_all('test')
        os.remove('minute')

    def test_hour_and_min_crontab(self):
        set_execution = getattr(set_cron_job, 'set_execution')
        # test hour and minures
        cwd = os.getcwd()
        test_file = open('minuteAndHour', 'w')
        test_file.close()
        command = "test " + cwd
        set_execution(command, 'minuteAndHour', True, hour=3, minute=2)

        user_cron  = CronTab(user=True)
        for line in user_cron.lines:
            if 'minuteAndHour' in line:
                self.assertEqual('3 2 * * * '+os.path.dirname(os.path.abspath(test_file)), line, 'checking hour and min timing\t...failed')
                user_cron.remove_all('test')
        os.remove('minuteAndHour')

if __name__ == '__main__':
    print ("Please check your cron tab \n use crontab -e command and remove all the entries that has \'test\'' in them")
    unittest.main() 