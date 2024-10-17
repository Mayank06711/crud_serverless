import json
from .db import get_db_connection

def get_users(event, context):
    conn = get_db_connection()
    if not conn:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to database"}),
        }

    try:
        cursor = conn.cursor()

        # Geting the request body and validate JSON
        body = event.get("body", "{}")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid JSON format"}),
                }

        # Retrieving and  filtering parameters
        user_id = body.get("user_id")
        mob_num = body.get("mob_num")
        manager_id = body.get("manager_id")

        # Start building the query
        query = "SELECT * FROM users"
        params = []
        conditions = []

        # Add conditions based on provided parameters
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        
        if mob_num:
            mob_num = mob_num.replace("+91", "").replace(" ", "").strip()
            conditions.append("mob_num = %s")
            params.append(mob_num)
        
        if manager_id:
            conditions.append("manager_id = %s")
            params.append(manager_id)

        # If there are conditions, append them to the query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        print("Executing query:", query)  # Debugging output
        print("With params:", params)  # Debugging output

        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        print("Rows fetched:", rows)  # Debugging output

        # Process the fetched rows
        users = []
        for row in rows:
            users.append( # Adding new dictionary (i mean single user) to the users array
                {
                    "user_id": row[0],
                    "full_name": row[1],
                    "mob_num": row[2],
                    "pan_num": row[3],
                    "manager_id": row[4],
                    "created_at": row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else None, #convert timestamp to make it readable
                    "updated_at": row[6].strftime("%Y-%m-%d %H:%M:%S") if row[6] else None,
                    "is_active": row[7],
                }
            )

        # Return the response
        return {"statusCode": 200, "body": json.dumps({"users": users})}
    
    except Exception as e:
        print("Error in get_users function:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "An error occurred while fetching users", "error": e}),
        }
    
    finally:
        if cursor:
            cursor.close()  # Close the cursor to release the memory/resources used for the query
        if conn:
            conn.close()  # Close the connection to free up the database connection pool

