import json
from .create_user import create_user
from .get_user import get_users
from .update_user import update_User
from .delete_user import delete_User

def route_handler(event, context):
    # Check the HTTP method and path from the event
    print(f"evenst\n {event}:context\n{context}")
    path = event.get("rawPath")
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if path == "/create_user" and method == "POST":
        return create_user(event, context)
    elif path == "/get_users" and method == "GET":
        return get_users(event, context)
    elif path == "/update_user" and method == "PUT":
        return update_User(event, context)
    elif path == "/delete_user" and method == "DELETE":
        return delete_User(event, context)
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"Error": f"No Such 'route' {path} exist, try again."})
        }
