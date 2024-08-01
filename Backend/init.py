import shutil
from server_pkg.server.app import create_app, db
from flask_migrate import upgrade, migrate, init, stamp
from server_pkg.server.models import User
from server_pkg.server.app import bcrypt
from server_pkg.server_db_manager import DB_Manager
import os
from getpass import getpass
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils

def cleanup():
    # remove migrations folder, UserDB.db and UserData.db if they exist
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        print("cleaned migrations")
    if os.path.exists("server_pkg/server/UserDB.db"):
        os.remove("server_pkg/server/UserDB.db")
        print("cleaned UserDB.db")
    if os.path.exists("server_pkg/UserData.db"):
        os.remove("server_pkg/UserData.db")
        print("cleaned UserData.db")

def deploy():
    """Run deployment tasks."""
    app = create_app()[0]
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()

def init_admin():
    email = input("Enter email for admin\t: ")
    pwd = getpass("Enter password for admin\t: ")
    ph_no = input("Enter phone number for admin\t: ")    
    username = "Server Admin"
    user_type = "A"

    Admin = User(
                    username=username,
                    email=email,
                    ph_no=ph_no,
                    pwd=bcrypt.generate_password_hash(pwd),
                    user_type=user_type,
                    category="",
                    niche="",
                    followers=0,
                    industry="",
                    budget=0)

    db.session.add(Admin)
    db.session.commit()

def init_ServerDB():
    DB_Manager().TableCreation()


prompt = input("""This script will reset the server.\nDo you want to continue [Y]/[n]: """)
if prompt == "Y":
    cleanup()
    deploy()
    init_admin()
    init_ServerDB()
else: 
    print("exiting the script")

