"""
Imports required for the program
================================
  read_parquet => Function to read the content of ".parquet" file into a dataframe.
  read_csv => Function to read the content of ".csv" file into a dataframe.
  sys => Module required to access command line arguments, which would contain path to files or URLs to files.
  dump => Function required to convert an object into standard json object.
  pyarrow => Engine required to parse parquet files.
"""

from pandas import read_parquet, read_csv
import sys
from json import dump
import pyarrow


def process_data(students, teachers):
    """
    Traverse the dataframes and maps the teachers to the students via the class_id, i.e., "cid" and then convert it into standard json object
    and store it in "output.json" file

    @params: students {Dataframe} - dataframe containing students' data from "students.csv" file
    @params: teachers {Dataframe} - dataframe containing teachers' data from "teachers.parquet" file

    @returns: None   
    """
    json_result = []
    for row in teachers.itertuples(index = True, name ='Pandas'):
        teacher_obj = {'teacher_id': getattr(row, 'id'),
                       'teacher_name': getattr(row, 'fname') + ' ' + getattr(row, 'lname'),
                       'class_id': getattr(row, 'cid')}

    for _, row in teachers.iterrows():
        teacher_obj = {'teacher_id': row['id'],
                       'teacher_name': row['fname'] + ' ' + row['lname'],
                       'class_id': row['cid']}

        student_det = []
        for _, _row in students[students['cid'] == row['cid']].iterrows():
            obj = {'student_id': _row['id'],
                   'student_name': _row['fname'] + ' ' + _row['lname']}
            student_det.append(obj)

        teacher_obj['students'] = student_det
        json_result.append(teacher_obj)

    try:
        with open('output.json', 'w') as outfile:
            dump(json_result, outfile, indent=4)
        print('Task Done, Successfully output.json file generated')
    except Exception as ex:
        print('Enable to create output.json')


"""
Driver code
===========
Description => Data Acquisition is done here and then the process_data function is called with corresponding dataframe objects.
               Here based on the type of command line arguments passed, data acquisition is done respectively.
                  Case 1: If number of command line arguments is equal to one, i.e., only command is present, it will check for files in
                          the same folder, if present process_data called else message displayed to user.
                  Case 2: If command line arguments contains the file urls (of S3 bucket) along with the credentials.
                  Case 3: If the command line arguments contains the absolute paths of the files.
"""
if __name__ == "__main__":

    if len(sys.argv) == 1:
        try:
            teachers = read_parquet('../dataset/teachers.parquet')
            students = read_csv('../dataset/students.csv', delimiter='_')
            process_data(students, teachers)
        except Exception as ex:
            print('Files not found, please enter paths or urls in command line arguments')
    else:
        if len(sys.argv) > 1 and sys.argv[1] == 's3':
            from smart_open import smart_open
            try:
                aws_id = sys.argv[2]
                aws_secret = sys.argv[3]
                bucket_name = sys.argv[4]
                object_key_teacher = 'teachers.parquet' if (
                    len(sys.argv) == 5) else sys.argv[5]
                object_key_student = 'students.csv'if (
                    len(sys.argv) == 5) else sys.argv[6]

                path = 's3://{}:{}@{}/{}'.format(aws_id,
                                                 aws_secret, bucket_name, object_key_teacher)
                teachers = read_parquet(smart_open(path), engine='pyarrow')

                path = 's3://{}:{}@{}/{}'.format(aws_id,
                                                 aws_secret, bucket_name, object_key_student)
                students = read_csv(smart_open(path), delimiter='_')

                process_data(students, teachers)

            except Exception as ex:
                print('something went wrong try again')

        elif sys.argv[1] != 's3':
            try:
                teachers = read_parquet(sys.argv[1], engine='pyarrow')
                students = read_csv(sys.argv[2], delimiter='_')
                process_data(students, teachers)
            except Exception as ex:
                print('Files not found, please enter paths or urls in command line arguments')
