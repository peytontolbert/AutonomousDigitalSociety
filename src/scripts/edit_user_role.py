from app import db, User

# Replace 'your_username' with the actual username of the user you want to edit
username_to_edit = 'your_username'

# Find the user by username
user = User.query.filter_by(username=username_to_edit).first()

if user:
    # Update the user's role to 'admin'
    user.role = 'admin'
    db.session.commit()
    print(f"User {username_to_edit}'s role has been updated to 'admin'.")
else:
    print(f"User {username_to_edit} not found.")

