import os
import shutil

def start(project_name):
    if not project_name:
        print("Project name cannot be empty.")
        return

    if os.path.exists(project_name):
        print(f"Directory '{project_name}' already exists.")
        return

    shutil.copytree("django_template", project_name)
    print(f"Django template copied to '{project_name}' directory.")
    return project_name

