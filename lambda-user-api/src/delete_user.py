import json
from db import get_db_connection

def delete_User(event, context):
    # Establish database connection
    conn = get_db_connection()
    if not conn:
        return {
            "statusCode": 500,
            "body": json.dumps({"Error": "Couldn`t not connect to database"}),
        }

    try:
        cursor = conn.cursor()

        # Parsing the request body
        body = json.loads(event.get("body", "{}"))
        user_id = body.get("user_id")
        mob_num = body.get("mob_num")

        # Checking for missing fields
        if not user_id and not mob_num:
            return {
                "statusCode": 400,
                "body": json.dumps({"Error": "user_id or mob_num is not provided"}),
            }

        # Performing the deletion
        if user_id:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,)) # It was more efficient to just deactivate user rather than deleting user, but did as per isntructions
        elif mob_num:
            # Normalize the mobile number, means replace +91 an spaces
            mob_num = mob_num.replace("+91", "").replace(" ", "").strip()
            cursor.execute("DELETE FROM users WHERE mob_num = %s", (mob_num,))

        # Check if any rows were affected
        if cursor.rowcount == 0:
            return {"statusCode": 404, "body": json.dumps({"error": "User not found in our database", "user_id": user_id})}

        # finaly saving all the changes during this transaction to the database
        conn.commit() 
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User successfully deleted", "user_id": user_id}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
    finally:
        # Ensuring the cursor and connection are closed, regardless of success or failure
        if cursor:
            cursor.close()
        if conn:
            conn.close()
