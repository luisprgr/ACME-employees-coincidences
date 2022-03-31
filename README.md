ACME-employees-coincidences
===========================
Programming exercise sent by ioet Inc.

## Description

The company ACME offers their employees the flexibility to work the hours they want. But due to some external circumstances they need to know what employees have been at the office within the same time frame

The goal of this exercise is to output a table containing pairs of employees and how often they have coincided in the office.

Input: the name of an employee and the schedule they worked, indicating the time and hours. This should be a .txt file with at least five sets of data. You can include the data from our examples below:

### Example 1:

INPUT
```
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00- 21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
```

OUTPUT:
```
ASTRID-RENE: 2
ASTRID-ANDRES: 3
RENE-ANDRES: 2
```
### Example 2:

INPUT:
```
RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
```

OUTPUT:
```
RENE-ASTRID: 3
```

## Solution

### Design Patterns used

* Object Oriented pattern
* Facade Pattern 

### Solution description

My solution basically consists of the following steps:

1) Analyze the input for errors before parsing
2) Convert the lines with the user information into "employee" objects that store the name and the schedule 
3) From these objects I analyze the cases where the schedules of two employees indicate that they are in the office at the same time, these cases are:
- The schedules are exactly the same
- The beginning of the first schedule is between the beginning and the end of the second one
- The end of the first schedule is between the start and end of the second schedule 
- The beginning of the second schedule is between the beginning and the end of the first schedule
- The end of the second schedule is between the beginning and the end of the first schedule 
- The first schedule is between the times of the second schedule
- The second schedule is between the times of the first schedule

    If the employees' schedules fall into these cases increase their overlaps by one

4) All these processes are stored and performed from a class "EmployeesScheduleComparator" that gives to the programmer who will use the class a simple way to perform the above mentioned processes and would also allow to reuse these processes with other types of inputs, besides the .txt file, since the logic for data input is separated from its processing.


## How to run the code

### Requirements:

* Python ( >= 3.8.10)

### Use

The project is executed with:

```
python3 main.py "path_to_the_employee_data_relative_to_main.py"
```

Example:

```
python3 main.py "employees.txt"
```
### Test

You can run the tests with:

```
python3 main.py test
```

## License

Licensed under the [MIT License](LICENSE) 