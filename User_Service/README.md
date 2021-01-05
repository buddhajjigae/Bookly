# user_services

# endpoint to show all users
/users, methods=["GET"]
curl http://localhost:8000/users -X GET

# endpoint to create new user
/users, methods=["POST"]
curl http://localhost:8000/users \
-X POST \
-H "Content-Type: application/json" \
 -d '{"email":"yy2608@columbia.edu", "password": "EUpgBHb", "last_name": "Yang", "first_name":"Yuechen"}'

# endpoint to get user detail by id
/users/<id>, methods=["GET"]
curl http://localhost:8000/users/1 -X GET

# endpoint to update user
/users/<id>, methods=["PUT"]
curl http://localhost:8000/users/1 \
-X PUT \
-H "Content-Type: application/json" \
 -d '{"email":"yuechen.yang@columbia.edu"}'
 
# endpoint to delete user
/users/<id>, methods=["DELETE"]
curl http://localhost:8000/users/0 \
-X DELETE