import subprocess
import shlex
import os
from src.config.config import MYSQL_DB


def insert_test_result_to_mysql(test_name, status, duration, timestamp):
    """
    Inserts a test result into the MySQL database using direct MySQL commands.
    Assumes the database and table already exist in the mysql-qa Docker container.

    Args:
        test_name (str): Name of the test case
        status (str): Status of the test ('passed' or 'failed')
        duration (float): Duration of the test execution in seconds
        timestamp (datetime.datetime): Timestamp of the test execution (UTC)
    """
    try:
        # Format timestamp for MySQL
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Escape single quotes in strings to prevent SQL injection
        safe_test_name = test_name.replace("'", "''")
        safe_status = status.replace("'", "''")
        
        # Use Docker exec to run MySQL command inside the container
        docker_cmd = f"""docker exec mysql-qa mysql -u {MYSQL_DB['user']} -p{MYSQL_DB['password']} \
                      {MYSQL_DB['database']} -e "INSERT INTO {MYSQL_DB['table']} \
                      (test_name, status, duration, timestamp) VALUES \
                      ('{safe_test_name}', '{safe_status}', {float(duration)}, '{formatted_timestamp}');"
                   """
                  
        # Execute the Docker MySQL command
        process = subprocess.Popen(
            shlex.split(docker_cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Get output and error (if any)
        _, stderr = process.communicate()
        
        # Check if there was an error
        if process.returncode != 0:
            error_message = stderr.decode('utf-8').strip()
            print(f"⚠️ MySQL command error: {error_message}")
            return
            
        print(f"📊 Test result saved to mysql-qa database: {test_name} | {status} | {duration:.2f}s")
            
    except Exception as e:
        print(f"⚠️ Error saving test result: {e}") 