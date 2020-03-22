import json
import os
from mylang import *


if "STARTUP_SUCCEED" not in globals():

    stat_directory = "D:\\Projects\\Code_Observer\\Statistics"
    config_file_path = "D:\\Projects\\Code_Observer\\project_directory_config.json"

    try:
        os.makedirs(stat_directory)
    except FileExistsError:
        pass

    # Load project data from config and create directories for them
    config_file_data = json.loads(open(config_file_path, "r").read())
    projects_config_data = config_file_data["projects"]
    common_code_extensions = config_file_data["extensions"]
    stat_file_capacity = config_file_data["stat_file_capacity"]

    project_stat_dirs = os.listdir(stat_directory)
    for _project in projects_config_data:
        if _project["name"] not in project_stat_dirs:
            os.mkdir(os.path.join(stat_directory, _project["name"]))
        if not os.listdir(os.path.join(stat_directory, _project["name"])):
            open(os.path.join(stat_directory, _project["name"], "1.json"), "w").close()
        temp_file0 = open(os.path.join(stat_directory, _project["name"], "1.json"), "r")
        if not temp_file0.read().strip():
            temp_file1 = open(os.path.join(stat_directory, _project["name"], "1.json"), "w")
            temp_file1.write("[\n\t\n]")
            temp_file1.close()
        temp_file0.close()


    project_data = []

    for _project in projects_config_data:
        project_data.append({
            "name" : _project["name"],
            "directories" : [_project["Directory_Root"]] if "Directory_Root" in _project else _project["directories"],
            "stat_dir" : os.path.join(stat_directory, _project["name"]),
            "extensions" : common_code_extensions if "additional_extensions" not in _project else list(set(common_code_extensions + _project["additional_extensions"]))
        })

    print_good_info("Data from Config file loaded and processed successfully!")
    # print(json.dumps(project_data, indent = 4))

STARTUP_SUCCEED = True
