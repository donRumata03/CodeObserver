from mylang import *
from startup import *

def find_last_temp_name(project_object : dict) -> str:
    existing_files = sorted(list(map(lambda f: int(f[:-len(".json")]), os.listdir(project_object["stat_dir"]))))
    last_file_index = existing_files[-1]
    last_file_name = str(last_file_index) + ".json"
    last_file_content = json.loads(open(os.path.join(project_object["stat_dir"], last_file_name), "r").read())
    last_file_length = len(last_file_content)
    this_storage_name = last_file_name
    if last_file_length > stat_file_capacity:
        this_storage_name = str(last_file_index + 1) + ".json"

    return this_storage_name

def find_last_temp_path(project_object : dict) -> str:
    return os.path.join(project_object["stat_dir"], find_last_temp_name(project_object))


def load_last_proj_temp(proj_obj : dict) -> Dict:
    all_pr_data = json.loads(open(find_last_temp_path(proj_obj), "r").read())
    return all_pr_data[-1]

def select_project_by_name(all_projects : List[dict], project_name : str) -> Optional[dict]:
    for pr in all_projects:
        if pr["name"] == project_name:
            return pr

    return None

if __name__ == '__main__':
    print_as_json(load_last_proj_temp(project_data[0]))