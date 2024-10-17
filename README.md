# crud_serverless
This is a assignment which I will most probably complete within two days.
This application follows infrastructure as a Code (IaaC) approach using serverless framework.

## Technology used:
- Serverless framework: For deploying and managing AWS Lambda functions.
- AWS-RDS (PostgreSQL as Database):A managed relational database service for handling user data.
- Python: The language used for writing the Lambda functions
- Any IDE (Like VSCode): For writing and editing code efficiently.

## Project Setup
Clone the Repository
```bash
git clone <your-repo-url>
cd lambda-user-api
```
## Prerequisites to 
Ensure the following tools are installed on your machine
 - Node.js: If not in your machine Download and install from its official website.
 - Serverless Framework: After installing Node.js, install the Serverless framework globally:
```bash
 npm install -g serverless
 ```
 AWS CLI: Install AWS CLI to configure your AWS credentials and run set up your credentials
 
```bash
 aws configure
```
 PostgreSQL: Install PostgreSQL and PgAdmin to interact with your RDS instance
  To Run Funtions Locally:
  ```bash
  serverless invoke local --function nameOfFuntions
  ```


 # AWS Lambda Layer Creation on Windows

Instructions on how to create and deploy an AWS Lambda Layer from scratch using a Windows machine.

## Steps to Create a Lambda Layer

### Create a Directory for Your Layer

Open PowerShell and run the following commands:

```powershell
mkdir my-layer
cd my-layer
mkdir python
```
## Install dependency that you want to use in your project.

```powershell
pip install psycopg2-binary -t python/
```
## Create a Zip File of the Layer

```powershell
cd .. 
Compress-Archive -Path .\my-layer\python\* -DestinationPath my-layer.zip
```
## Upload the Layer to AWS Lambda
Now there are two ways of deoing this one through  AWS Management Console  and one through aws-cli.
For  AWS Management Console.
- Open aws console and go to Lambda dashboard.
- Now go to layers section and click on it.
- Click on create layer.
- Give a name of your layer and add a short description.
- Click on upload zip file and upload the zip file that you just created (It will be in my-layer folder).
- Choose compatible runtime (like python 3.10 or 3.9 or 3.8 etc) you can choose more than one.
- Click on create button and it will be created.
Now you will see an Amazon Resource Name (arn) for your layer copy it.
This is the thing you will be using in you serverless.yaml file for layers that your lambda funtions will use.
## Using AWS-CLI
- For this you must have aws-cli installed and configured in your machine.
- For configuring you aws-cli you must have a your access key and access Secret key.
- **To get these keys** 
    - Open Console
    - Click on top most right corner where you username and accound id is shown.
    - Click on Security credentials
    - Scroll down and you will see Access Keys
    - Create one if you do not have one.
    - Copy Access Key and Access Secret key or download the keys.
Now open your terminal and run, and then enter your keys.
```aws-cli
aws configure
```
Now time to create layer using cli
```
aws lambda publish-layer-version --layer-name your-layer-name --description "your-layer-description" --zip-file fileb://my-layer.zip --compatible-runtimes python3.8 python3.9 python3.10
```
 Make sure to replace things starts with your- and run this command from your directory within which your my-layer.zip file is else you have to give provide the correct full path where your zip file 
 is stored in your machine.

 ## Database Setup
  - Create a PostgreSQL database instance from AWS RDS dashboard.
  - Note down the endpoint Database name username and password.
  - Install pgadmin and postgreSQL cli in your machine.
  - Run the below command to connect with your database with your terminal
   ```bash
    psql -h endpoint-you-copied -p 5432 -U username -d database
   ```
   If does not work (happened in my case, because was connecting without creating database) just replace username with postgres and database with postgres 
   and head over to your AWS-Console and open RDS (dashboard) and make sure its security group has inbound rules allowing postgreSQL with port 5432 and you can choose CIDR block either 0.0.0.0/0 
   (anywhere) or add your ip only.
   **NOTE** 
   If does not work please use any AI by copying pasting the error you got (Hide credentials like endpoint) in command.
   Now when you will enter the above thing it will ask for your password, make sure to enter your password.
   You will see something like this "yourDatabaseName->" in your cli.
   Run to see list of databases. 
   ```sql
   \l
   ```
  
  ## Create the following tables
   - users Table
     
     ```sql
     CREATE TABLE users (
         user_id UUID PRIMARY KEY,
         full_name VARCHAR(255) NOT NULL,
         mob_num VARCHAR(15) NOT NULL,
         pan_num VARCHAR(10) NOT NULL,
         manager_id UUID,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         is_active BOOLEAN DEFAULT TRUE
     );
     ```
     
  - managers Table

     ```sql
     CREATE TABLE managers (
         id UUID PRIMARY KEY,
         name VARCHAR(255) NOT NULL
     );
     ```
   Now to check tables run below command to see created tables, if not created it will not show.
   ```sql
    \dt
   ```
  Now since there is no route to create managers run the below command to create manager first or make one through AWS console in your database.
   ```sql
     INSERT INTO managers (id, name) VALUES 
     ('f47ac10b-58cc-4372-a567-0e02b2c3d479', 'John Doe');
   ```
  **NOTE Change ID since it might not be unique** 
  
## Connecting with database
But before moving forward in this section you must install psycopg2-binary either in your system or in your virtual environment to ensure your development environment is properly configured to use psycopg2 (use for connecting with database (PostgreSQL) it's a bridge between your Python application and your database).
We are installing psycopg2-binary because it is pre-compiled version of psycopg2, which makes it easier to install and use.
- *get_db_connection*:
  - This funtion is responsible for establishing a connection to the PostgreSQL database using the provided connection parameters such as host, 
    database, user, password, and port.
  - This funtion uses psycopg2 to connect with our RDs (postgreSQL)  database and return a connection object which represents an open connection 
    between our Python application and the PostgreSQL database essential for managing SQL queries and mamaging ransactions.
  - This connection object has a methods like cursor, which is used to execute SQL queries and considered as data element **you can have multiple 
    cursor on the same data within single connection and fetch results and commit use to commit final changes to 
    database close to close connection and rollback to roll back all transactions.

### Explanation of File Structure

- **crud_serverless/**: Root folder containing the project.
- **lambda-user-api/**: Contains all files related to the user API service.
- **src/**: Source directory where all the Python files for the Lambda functions will be located when packaged on deployment.

## Functions

### 1. **create_user**
- **Description**: This function creates a new user in the database.
- **File**: `create_user.py`
- **Key Features**:
  - Validates input data.
  - Checks for existing users before creation.
  - Utilizes a database connection established by `get_db_connection.py`.
  - Returns a success message or an error if the creation fails.

### 2. **get_users**
- **Description**: Retrieves user information based on specified criteria (user ID, mobile number, or manager ID).
- **File**: `get_users.py`
- **Key Features**:
  - Connects to the database to fetch user details.
  - Supports filtering by user ID, mobile number, or manager ID.
  - Returns user data in a structured format or an error message if the operation fails.

### 3. **update_user**
- **Description**: Updates user information in the database.
- **File**: `update_user.py`
- **Key Features**:
  - Validates user IDs and checks for their existence in the database.
  - Allows bulk updates for specific fields, primarily the manager ID.
  - Utilizes a database connection for executing update queries.
  - Returns a success message or an error for missing data or invalid operations.

### 4. **delete_user**
- **Description**: Deletes a user from the database.
- **File**: `delete_user.py`
- **Key Features**:
  - Validates user IDs before deletion.
  - Ensures that users are actually present in the database before attempting to delete.
  - Returns a confirmation message or an error if the deletion fails.

### 5. **handler**
- **Description**: This function could acts as the main entry point for routing API requests to the appropriate functions. However, it's important to note that this routing mechanism requires specific configurations in the `serverless.yml` file to work effectively. In this project, I opted not to use this monolithic approach because it can complicate deployment and maintenance. Instead, each API endpoint is handled by its dedicated function defined in the `serverless.yml` file, promoting better modularity and separation of concerns.

  This approach allows for:
  - **Independent Functionality**: Each function handles a specific task, making it easier to update and manage.
  - **Simplified Error Handling**: Errors can be caught and managed within each individual function, providing clearer feedback.
  - **Scalability**: Adding new features or endpoints can be done by simply creating new functions without altering the existing codebase.

  But since I wrote this with idea to use it thereby leaving it as it is in the `handler.py` file that I will be using as a reference point for understanding how requests could be routed in a different design and experiment with this, the current implementation prioritizes a clean, modular structure over a monolithic design.


## Deployment

The project is set up to be deployed using the Serverless Framework. The configuration is managed in the `serverless.yml` file, which defines the AWS Lambda functions, event triggers, environment variables, and other necessary settings.

- Run below command to deploy
 ```bash
 serverless deploy
 ```

### Environment Variables
Sensitive data such as database credentials are passed in serverless.yaml file so that it can be accessile to all lambda funtions when needed alternatively we could ave used AWS Systems Manager (SSM) Parameter Store, this enhance security. The environment variables defined in `serverless.yml` include:
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`

## Best Practices I Used 
- **Closing Cursors**: Each function that interacts with the database ensures that cursors are properly closed after operations to prevent resource leaks and improve performance.
- **Error Handling**: Each function includes error handling to manage different types of errors gracefully, providing meaningful responses to the client.
- **Modularity**: Functions are kept modular and focused on specific tasks, making the codebase easier to maintain and extend.

### Solution Of Problem You May Face After Deployment (If Your layer arn not working)
Use requirements.txt for Dependency Management of your application

 **Create requirements.txt**: 
 -Add the dependencies needed for the project, like psycopg2-binary, in the requirements.txt file.

```bash
npm install --save serverless-python-requirements@latest
```

```bash
 pip install -r requirements.txt
```
 
## Conclusion

This serverless user crud APi provides a robust framework for managing user data in a scalable and efficient manner. Each function is designed to handle specific tasks, allowing for clear separation of concerns and improved maintainability.



