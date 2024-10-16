# crud_serverless
This is a assignment which I will most probably complete within two days.
This application follows infrastructure as a Code (IaaC) approach using serverless framework.

## Technology used:
- Serverless framework
- AWS-RDS (PostgreSQL as Database)
- Python 
- Any IDE (Like VSCode)

## Features
- Create, read, update, and delete (CRUD) operations for user records
- Utilizes AWS Lambda functions for serverless computing
- Connects to a PostgreSQL database hosted on Amazon RDS
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



