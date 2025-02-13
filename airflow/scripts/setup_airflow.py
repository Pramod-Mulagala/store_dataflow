import os
import subprocess
from pathlib import Path

def setup_airflow():
    # Set Airflow home directory
    airflow_home = Path.home() / "airflow"
    os.environ["AIRFLOW_HOME"] = str(airflow_home)
    
    # Create necessary directories
    directories = [
        airflow_home / "dags",
        airflow_home / "plugins",
        airflow_home / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    print("Airflow directory structure created successfully!")

if __name__ == "__main__":
    setup_airflow() 