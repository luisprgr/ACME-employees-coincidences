import datetime
import re
from components.hour import Hour
from components.employee import Employee


class EmployeesScheduleComparator:

    def employees_schedule_comparator(self, employees_schedule_data):
        """returns the coincidences in a employee's schedule list"""

        response = ''

        if len(employees_schedule_data) > 1:
            employees = self.employee_strings_parser(employees_schedule_data)

            combinations = self.employee_combinations(
                [employee_name for employee_name in employees])

            coincidences = self.employee_comparator(employees, combinations)

            for employee, coincidence in zip(combinations, coincidences):
                response += employee[0] + '-' + \
                    employee[1] + ': ' + str(coincidence) + '\n'
        else:
            raise Exception('It is necessary to have more than one employee')

        return response.rstrip()

    def employee_strings_parser(self, employee_strings):
        """reads the lines with the employee's data and returns a dictionary with employee objects"""
        employees = dict()
        for line in employee_strings:
            line = line.rstrip()
            if (self.employee_string_validator(line)):
                employee_name, schedule_line = line.split('=')
                if (self.schedule_month_validator(schedule_line)):
                    employee = Employee(
                        employee_name, self.schedule_parser(schedule_line))
                    employees[employee_name] = employee
                else:
                    raise Exception(
                        'the days in the employee schedule are not correct')
            else:
                raise Exception('there is invalid data in the input data')
        return employees

    def employee_string_validator(self, employee_string):
        """validates that the line with an employee's data has the correct formatting"""
        if re.match('^([A-Z]+=(((MO|TU|WE|TH|FR|SA|SU)((0|1)[0-9]|2[0-3]):([0-5][0-9])-((0|1)[0-9]|2[0-3]):([0-5][0-9]),?){1,7}))$', employee_string):
            return True
        else:
            return False

    def schedule_month_validator(self, schedule):
        """validates if there are no repeating days in an employee's schedule"""
        if schedule.count('MO') > 1 or schedule.count('TU') > 1 or schedule.count('WE') > 1 or schedule.count('TH') > 1 or schedule.count('FR') > 1 or schedule.count('SA') > 1 or schedule.count('SU') > 1:
            return False
        else:
            return True

    def schedule_parser(self, schedule):
        """reads the schedule string of a employee and return a dictionary with the schedule"""
        schedule_dict = dict()
        for line in schedule.split(','):
            day = line[:2]
            start, end = self.time_parser(line[2:])
            schedule_dict[day] = Hour(start, end)
        return schedule_dict

    def time_parser(self, hours):
        """reads a string with the time ranges of the schedule, and return a start and end datetime objects"""
        start, end = hours.split('-')
        return [datetime.datetime.strptime(start, '%H:%M').time(), datetime.datetime.strptime(end, '%H:%M').time()]

    def employee_combinations(self, employee_list):
        combinations = []
        for i in range(len(employee_list) - 1):
            for j in range(i + 1, len(employee_list)):
                combinations.append([employee_list[i], employee_list[j]])
        return combinations

    def employee_comparator(self, employees, combinations):
        """returns a list of coincidences in schedules for a list of pairs of employees"""
        coincidences = []

        for employee1, employee2 in combinations:
            schedule_employee1 = employees[employee1].schedule
            schedule_employee2 = employees[employee2].schedule
            coincidences.append(self.schedule_comparator(
                schedule_employee1, schedule_employee2))

        return coincidences

    def schedule_comparator(self, schedule1, schedule2):
        """compares the schedules of two employees and returns how many coincidences they have had"""
        coincidences = 0
        for day in ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']:
            if (day in schedule1) and (day in schedule2):
                sch1_start = schedule1[day].start
                sch1_end = schedule1[day].end
                sch2_start = schedule2[day].start
                sch2_end = schedule2[day].end
                if (sch1_start >= sch2_start) and (sch1_start <= sch2_end):
                    coincidences += 1
                elif (sch1_end >= sch2_start) and (sch1_end <= sch2_end):
                    coincidences += 1
                elif (sch2_start >= sch1_start) and (sch2_start <= sch1_end):
                    coincidences += 1
        return coincidences
