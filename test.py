import datetime
import unittest
from components.employee import Employee
from components.hour import Hour
from employees_schedules_comparator import EmployeesScheduleComparator


class TimeComparatorTest(unittest.TestCase):

    def test_employee_string_validator(self):
        e = EmployeesScheduleComparator()
        self.assertTrue(e.employee_string_validator(
            'JUAN=MO07:00-12:00,TU00:00-05:00,WE09:00-21:00'))
        self.assertFalse(e.employee_string_validator(
            'JUAN=MI07:00-12:00,TU00:00-05:00,WE09:00-21:00'))
        self.assertFalse(e.employee_string_validator(
            'JUAN=MO70:00-12:00,TU00:00-05:00,WE09:00-21:00'))
        self.assertFalse(e.employee_string_validator(
            '=MO07:00-12:00,TU00:00-05:00,WE09:00-21:00'))
        self.assertFalse(e.employee_string_validator(
            'JUAN=MO07:00-12:00,TU00:0005:00,WE09:00-21:00'))

    def test_schedule_month_validator(self):
        e = EmployeesScheduleComparator()
        self.assertTrue(e.schedule_month_validator(
            'MO07:00-12:00,TU00:00-05:00,WE90:00-21:00'))
        self.assertFalse(e.schedule_month_validator(
            'MO07:00-12:00,MO00:00-05:00,WE90:00-21:00'))

    def test_time_parser(self):
        e = EmployeesScheduleComparator()
        self.assertEqual(e.time_parser('00:00-14:00'), [datetime.datetime.strptime('00:00', '%H:%M').time(),
                                                        datetime.datetime.strptime('14:00', '%H:%M').time()])
                                            
    def test_employee_combinations(self):
        e = EmployeesScheduleComparator()
        self.assertEqual(e.employee_combinations(['A','B','C']),[['A','B'],['A','C'],['B','C']])

    def test_schedule_comparator(self):
        e = EmployeesScheduleComparator()

        # exactly the same schedules

        schedule1 = dict()
        schedule1['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                               datetime.datetime.strptime('14:00', '%H:%M').time())
        schedule2 = dict()
        schedule2['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                               datetime.datetime.strptime('14:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule1, schedule2), 1)

        # start of schedule 1 between schedule 2

        schedule3 = dict()
        schedule3['MO'] = Hour(datetime.datetime.strptime('09:00', '%H:%M').time(),
                               datetime.datetime.strptime('15:00', '%H:%M').time())
        schedule4 = dict()
        schedule4['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                               datetime.datetime.strptime('14:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule3, schedule4), 1)

        # start of schedule 2 between schedule 1

        schedule5 = dict()
        schedule5['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                               datetime.datetime.strptime('14:00', '%H:%M').time())
        schedule6 = dict()
        schedule6['MO'] = Hour(datetime.datetime.strptime('10:00', '%H:%M').time(),
                               datetime.datetime.strptime('20:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule5, schedule6), 1)

        # end of schedule 1 between schedule 2

        schedule7 = dict()
        schedule7['MO'] = Hour(datetime.datetime.strptime('06:00', '%H:%M').time(),
                               datetime.datetime.strptime('12:00', '%H:%M').time())
        schedule8 = dict()
        schedule8['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                               datetime.datetime.strptime('14:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule7, schedule8), 1)

        # end of schedule 2 within schedule 1

        schedule9 = dict()
        schedule9['MO'] = Hour(datetime.datetime.strptime('09:00', '%H:%M').time(),
                               datetime.datetime.strptime('15:00', '%H:%M').time())
        schedule10 = dict()
        schedule10['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                datetime.datetime.strptime('10:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule9, schedule10), 1)

        # schedule 1 in schedule 2

        schedule11 = dict()
        schedule11['MO'] = Hour(datetime.datetime.strptime('12:00', '%H:%M').time(),
                                datetime.datetime.strptime('13:00', '%H:%M').time())
        schedule12 = dict()
        schedule12['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                datetime.datetime.strptime('14:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule11, schedule12), 1)

        # schedule 2 in schedule 1

        schedule13 = dict()
        schedule13['MO'] = Hour(datetime.datetime.strptime('09:00', '%H:%M').time(),
                                datetime.datetime.strptime('15:00', '%H:%M').time())
        schedule14 = dict()
        schedule14['MO'] = Hour(datetime.datetime.strptime('10:00', '%H:%M').time(),
                                datetime.datetime.strptime('11:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule13, schedule14), 1)

        # different schedules

        schedule15 = dict()
        schedule15['MO'] = Hour(datetime.datetime.strptime('09:00', '%H:%M').time(),
                                datetime.datetime.strptime('15:00', '%H:%M').time())
        schedule16 = dict()
        schedule16['MO'] = Hour(datetime.datetime.strptime('16:00', '%H:%M').time(),
                                datetime.datetime.strptime('22:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule15, schedule16), 0)

        # same hours different days

        schedule17 = dict()
        schedule17['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                datetime.datetime.strptime('14:00', '%H:%M').time())
        schedule18 = dict()
        schedule18['TU'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                datetime.datetime.strptime('14:00', '%H:%M').time())

        self.assertEqual(e.schedule_comparator(schedule17, schedule18), 0)

    def test_schedule_parser(self):
        e = EmployeesScheduleComparator()
        schedule = dict()
        schedule['SA'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                              datetime.datetime.strptime('20:00', '%H:%M').time())
        schedule['SU'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                              datetime.datetime.strptime('20:00', '%H:%M').time())
        self.assertEqual(e.schedule_parser(
            "SA07:00-20:00,SU07:00-20:00"), schedule)
        self.assertNotEqual(e.schedule_parser(
            "MO07:00-20:00,SU08:00-20:00"), schedule)

    def test_employee_strings_parser(self):
        e = EmployeesScheduleComparator()

        employee_string = ['ANA=MO07:00-12:00,SU00:00-07:00',
                           'MARIA=MO10:00-14:00,TH12:00-14:00']

        employee_string2 = ['LUIS=MO07:00-12:00,SU00:00-07:00',
                            'BELEN=TU00:00-07:00,TH12:00-14:00']

        employees = dict()

        ana_schedule = dict()
        ana_schedule['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                  datetime.datetime.strptime('12:00', '%H:%M').time())
        ana_schedule['SU'] = Hour(datetime.datetime.strptime('00:00', '%H:%M').time(),
                                  datetime.datetime.strptime('07:00', '%H:%M').time())
        employees['ANA'] = Employee('ANA', ana_schedule)

        maria_schedule = dict()
        maria_schedule['MO'] = Hour(datetime.datetime.strptime('10:00', '%H:%M').time(),
                                    datetime.datetime.strptime('14:00', '%H:%M').time())
        maria_schedule['TH'] = Hour(datetime.datetime.strptime('12:00', '%H:%M').time(),
                                    datetime.datetime.strptime('14:00', '%H:%M').time())
        employees['MARIA'] = Employee('MARIA', maria_schedule)

        self.assertEqual(e.employee_strings_parser(employee_string), employees)
        self.assertNotEqual(e.employee_strings_parser(
            employee_string2), employees)

    def test_employee_comparator(self):
        e = EmployeesScheduleComparator()

        employees = dict()
        juan_schedule = dict()
        juan_schedule['MO'] = Hour(datetime.datetime.strptime('07:00', '%H:%M').time(),
                                   datetime.datetime.strptime('15:00', '%H:%M').time())
        juan_schedule['TU'] = Hour(datetime.datetime.strptime('08:00', '%H:%M').time(),
                                   datetime.datetime.strptime('20:00', '%H:%M').time())
        juan_schedule['WE'] = Hour(datetime.datetime.strptime('08:00', '%H:%M').time(),
                                   datetime.datetime.strptime('20:00', '%H:%M').time())
        employees['JUAN'] = Employee('JUAN', juan_schedule)

        pablo_schedule = dict()
        pablo_schedule['MO'] = Hour(datetime.datetime.strptime('09:00', '%H:%M').time(),
                                    datetime.datetime.strptime('17:00', '%H:%M').time())
        pablo_schedule['TU'] = Hour(datetime.datetime.strptime('12:00', '%H:%M').time(),
                                    datetime.datetime.strptime('20:00', '%H:%M').time())
        pablo_schedule['TH'] = Hour(datetime.datetime.strptime('12:00', '%H:%M').time(),
                                    datetime.datetime.strptime('20:00', '%H:%M').time())
        employees['PABLO'] = Employee('PABLO', pablo_schedule)

        combinations = [['PABLO', 'JUAN']]

        self.assertEqual(e.employee_comparator(employees, combinations), [2])

    def test_employees_schedule_comparator(self):
        e = EmployeesScheduleComparator()

        employees_schedule_data = ['RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00',
                                   'ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00']

        expected_response = 'RENE-ASTRID: 3'

        self.assertEqual(e.employees_schedule_comparator(employees_schedule_data),
                         expected_response)
