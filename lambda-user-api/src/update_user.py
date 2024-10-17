from datetime import datetime, timezone
import json
from db import get_db_connection

def update_User(event, context):
    # Establish database connection
    conn = get_db_connection()
    if not conn:
        return {
            "statusCode": 500,
            "body": json.dumps({"Error": "Couldn`t connect to the database"}),
        }

    cursor = conn.cursor()
    try:
        # Parsing the request body
        body = json.loads(event.get("body", "{}"))
        user_ids = body.get("user_ids")
        update_data = body.get("update_data")

        # Validating the input
        if not user_ids or not update_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"Error": "User_ids or update_data is not provided."}),
            }

        # Check if the provided user IDs exist in the users table
        cursor.execute("SELECT user_id FROM users WHERE user_id IN %s", (tuple(user_ids),))
        old_user_ids = {row[0] for row in cursor.fetchall()}
        
        not_found_user_ids = set(user_ids) - old_user_ids
        if not_found_user_ids:
            return {
                "statusCode": 404,
                "body": json.dumps({"Error": f"User IDs {', '.join(map(str, not_found_user_ids))} not found"}),
            }

        # Validate manager_id if present in update_data
        if "manager_id" in update_data:
            manager_id = update_data["manager_id"]
            cursor.execute("SELECT manager_id FROM managers WHERE manager_id = %s", (manager_id,))
            if not cursor.fetchone():
                return {
                    "statusCode": 400,
                    "body": json.dumps({"Error": "Manager ID does not exist in our database"})
                }

        # Prevent bulk updates for fields other than 'manager_id'
        if len(update_data) > 1 and "manager_id" not in update_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"Error": "Bulk updates are only allowed for manager_id"}),
            }

        # Process updates for each user ID
        for user_id in user_ids:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            if not row:
                continue  # Skip if user is not found (although this case shouldn't occur here)
            
            current_time = datetime.now(timezone.utc) 
            # Handle 'manager_id' updates
            if "manager_id" in update_data:
                if row[4]:  #  manager_id is oresent
                    # isActive ko false kar diya 
                    cursor.execute(
                        "UPDATE users SET is_active = FALSE, updated_at = %s WHERE user_id = %s", 
                        (current_time, user_id)
                    )
                # updating  with the new manager Id
                cursor.execute(
                    """
                    INSERT INTO users (user_id, full_name, mob_num, pan_num, manager_id, created_at, updated_at, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET manager_id = EXCLUDED.manager_id, updated_at = EXCLUDED.updated_at
                    """,
                    (
                        user_id,
                        row[1],  # full_name
                        row[2],  # mob_num
                        row[3],  # pan_num
                        update_data["manager_id"],  # New manager_id
                        row[5],  # created_at (original timestamp)
                        current_time,  # updated_at (current timestamp)
                        True,  # is_active
                    ),
                )
            else:
                # Handle other field updates (excluding manager_id)
                cursor.execute(
                    """
                    INSERT INTO users (user_id, full_name, mob_num, pan_num, manager_id, created_at, updated_at, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET full_name = EXCLUDED.full_name,
                        mob_num = EXCLUDED.mob_num,
                        pan_num = EXCLUDED.pan_num,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        user_id,
                        update_data.get("full_name", row[1]),  # Update full_name if provided, else use existing
                        update_data.get("mob_num", row[2]),  # Update mob_num if provided, else use existing
                        update_data.get("pan_num", row[3]),  # Update pan_num if provided, else use existing
                        row[4],  # manager_id remains unchanged
                        row[5],  # created_at
                        current_time,  # updated_at
                        True,  # is_active
                    ),
                )

        # Commit changes to the database
        conn.commit()
        return {
            "statusCode": 200,
            "body": json.dumps({"Message": "Succesfully updated the users"}),
        }
    except Exception as e:
        # Log the error for debugging purposes
        print("Hi got error in update_User function:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"Error": str(e)}),
        }
    finally:
        if cursor:
            cursor.close()  
        if conn:
            conn.close()  
