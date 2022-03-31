import sys
import unittest
from employees_schedules_comparator import EmployeesScheduleComparator

if __name__ == '__main__':

    if sys.argv[1] == 'test': 
        loader = unittest.TestLoader()
        suite = loader.discover('')
        runner_t = unittest.TextTestRunner()
        runner_t.run(suite)
    else:
        try:
            with open(sys.argv[1]) as f:
                comparator = EmployeesScheduleComparator()
                print(comparator.employees_schedule_comparator(f.readlines()))
        except Exception as e:
            print(e)
