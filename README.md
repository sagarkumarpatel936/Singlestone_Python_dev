# Task
An application that processes the two data files [students.csv , teachers.parquet]. The application should use both files to output a report in json listing each teacher with the students being taught by him / her.
The application will be used with both local files (where the absolute file paths will be passed via command line arguments) and files stored in aws S3 (where the credentials and the urls of files will be passed via command line arguments).

Also the code is written by considering an optimal tradeoff between the space and time complexity of the code and the optimal performance of the multiple approaches to perform the task.
 

# System requirements 
- OpenSSL 1.1.1
- python 3

 

# Modules used 
- os        : to access files from local directory
- json      : to output a proper json formatted data
- pyarrow   : to access parquet files 
- pandas    : for processing csv and parquet files
- botocore  : for accessing S3 bucket files and exception handling corresponding to S3 functionalities
 

# Set up environment 
### Create an environment 
```bash
python -m virtualenv task_env
```

 
### Activate environment 
```bash
source task_env/bin/activate
```

### Install requirements
```bash
pip install -r requirements.txt
```
 

# Commands to run 
### Git clone 
```git
git clone <url>
```

### Command to run 
```python
python3 -m venv /path/to/task_env        # could be any path
source /path/to/task_env/bin/activate
pip install -r requirements.txt
python3 src/app.py ./dataset/teachers.parquet ./dataset/students.csv # command line arguments 
```


### Docker commands 
```dockerfile
$ docker build -t username/my-app .
$ docker run --rm --name ss -e AWS_ACCESS_KEY_ID="your_access_key" -e AWS_SECRET_ACCESS_KEY="your_secrt_key" -e AWS_BUCKET_NAME="your_bucket_name" --name username/my-app
```
