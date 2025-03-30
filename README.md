# Insider Career QA Automation Tests

This project implements automated end-to-end UI tests for the Insider careers website, focusing on QA job positions in Istanbul.

## Project Structure

```
levo_qa_automation/
├── requirements.txt        # Project dependencies
├── run_tests.sh            # Script to run tests with proper setup
├── src/
│   ├── config/             # Configuration files
│   ├── core/               # Core functionality
│   │   └── base_page.py    # Base page class with common methods
│   ├── pages/              # Page objects
│   │   ├── home_page.py    # Insider home page
│   │   ├── careers_page.py # Careers page
│   │   └── qa_careers_page.py # QA careers page
│   ├── tests/              # Test scripts
│   │   ├── conftest.py     # Pytest configuration
│   │   └── test_insider_career.py # Test for career page flow
│   └── utils/              # Utility functions
│       └── db_controller.py # Database operations using Docker MySQL commands
└── screenshots/            # Test failure screenshots (created during test runs)
```

## Setup Instructions

1. Install Python 3.8 or higher

2. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up MySQL in Docker:
   - The test framework requires a MySQL Docker container named "mysql-qa"
   
   ### Create and Start the MySQL Container
   ```bash
   docker run --name mysql-qa \
     -e MYSQL_ROOT_PASSWORD=123qwe123 \
     -e MYSQL_DATABASE=test_results \
     -p 3306:3306 \
     -d mysql:8
   ```
   
   ### Create the Test Results Table
   ```bash
   docker exec -it mysql-qa mysql -u root -p123qwe123 test_results -e "
   CREATE TABLE IF NOT EXISTS ui_test_results (
       id INT AUTO_INCREMENT PRIMARY KEY,
       test_name VARCHAR(255) NOT NULL,
       status VARCHAR(50) NOT NULL,
       duration FLOAT NOT NULL,
       timestamp DATETIME NOT NULL
   );"
   ```
   
   ### Verify Database and Table Creation
   ```bash
   docker exec -it mysql-qa mysql -u root -p123qwe123 -e "
   SHOW DATABASES;
   USE test_results;
   SHOW TABLES;
   DESCRIBE ui_test_results;"
   ```
   
   ### Additional Docker Commands
   ```bash
   # Stop the MySQL container
   docker stop mysql-qa
   
   # Start the MySQL container again
   docker start mysql-qa
   
   # Remove the container (deletes all data)
   docker rm -f mysql-qa
   ```
   
   - The configuration in `src/config/config.py` is set to use:
     - host: mysql-qa (Docker container name)
     - user: root
     - password: 123qwe123
     - database: test_results
     - table: ui_test_results

4. Docker Requirements:
   - Docker must be installed and running
   - You must have permissions to execute `docker exec` commands
   - The mysql-qa container must be running when tests are executed

## Running the Tests

You can run the tests using the provided shell script:
```
cd levo_qa_automation
./run_tests.sh
```

Or run them directly with pytest:
```
cd levo_qa_automation
python -m pytest src/tests/test_insider_career.py -v
```

### Test Environment Options

- Tests run on both Chrome and Firefox by default
- Use `-v` flag for verbose output

## Test Case

The automated test performs the following steps:
1. Navigate to the Insider homepage
2. Accept cookies
3. Navigate to the Careers page
4. Verify required sections exist on the Careers page
5. Navigate to the QA Careers page
6. Click on "See all QA jobs" button
7. Filter jobs for Istanbul location
8. Verify job listings contain both QA and Istanbul
9. Verify the "View Role" button redirects to a job details page

## Reporting

- Test results are recorded in the MySQL database inside the mysql-qa Docker container
- The framework uses `docker exec` to execute MySQL commands inside the container
- Screenshots are automatically captured on test failures
- Console output provides detailed progress information 