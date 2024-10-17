import json
import uuid
import re

# importing db connection function, it is telling that from db file (which is at same directory level, bring get_db_connection funtion)
from .db import get_db_connection

def create_user(event, context):
    conn = get_db_connection()
    if not conn:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to database"}),
        }

    cursor = conn.cursor()

    try:
        body = json.loads(event.get("body", "{}"))
        full_name = body.get("full_name")
        mob_num = body.get("mob_num")
        pan_num = body.get("pan_num")
        manager_id = body.get("manager_id")

        if not full_name or not mob_num or not pan_num:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"}),
            }

        # Normalize mobile number, by extracting mobile number by replacing +91 and wtih "" and removing all trailing and leadaing spaces (strip) , 
        mob_num = mob_num.replace("+91", "").replace(" ", "").strip()
        if len(mob_num) != 10:
            return {
                
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid mobile number"}),
            }

        pan_num = pan_num.upper()
        
        # matching the pan format using regex (first 5 capital letters) then 4 numbers and then last one capital letter
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid PAN number"})}
        
        # Validate manager ID if provided
        if manager_id:
            cursor.execute("SELECT 1 FROM managers WHERE manager_id = %s", (manager_id,)) #,manager_id  is treated as a plain string and not executable code preventing from SQL injection.
            if cursor.fetchone() is None:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid manager ID"}),
                }

        # Check for duplicate mobile number or PAN number if already exists
        cursor.execute("SELECT 1 FROM users WHERE mob_num = %s OR pan_num = %s", (mob_num, pan_num))
        if cursor.fetchone() is not None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "User with this mobile number or PAN already exists"})
            }
        
        # generting uique user id
        user_id = str(uuid.uuid4())
        
        # Insert new user into the database
        cursor.execute(
            """
            INSERT INTO users (user_id, full_name, mob_num, pan_num, manager_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, full_name, mob_num, pan_num, manager_id),
        )
        
        #permanently save new user data in our, if fails rolls back all changes 
        conn.commit()
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "User created successfully"}),
        }
    except Exception as e:
        print("An error occured while creating user:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn:    
            conn.close() 

#NOTES:
# Once the connection is established, cursor() is used to interact with the database. A cursor object allows you to execute SQL queries and retrieve results from the database.
