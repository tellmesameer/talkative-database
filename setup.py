import os
import subprocess
import venv

venv_dir = "venv"

def set_virual_env():

    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("Virtual environment already exists.")

def install_requirements():
    pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")

    print("Installing requirements...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])

    print("Setup complete.")


# def create_tables():

#     with open("query/create.sql", "r") as file:
#         sql_script = file.read()
        
#     conn = sqlite3.connect("myDataBase.db")

#     cursor = conn.cursor()
#     cursor.executescript(sql_script)

#     print("Tables created successfully.")


if __name__ == "__main__":
    set_virual_env()
    install_requirements()
    # create_tables()
