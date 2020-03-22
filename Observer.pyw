from startup import *
from file_walker import *
from datetime import datetime
import data_base_processor


def get_project_data(project_object : dict):
    # Find proper file for writing data
    this_storage_path = data_base_processor.find_last_temp_path(project_object)
    if not os.path.exists(this_storage_path):
        temp_file2 = open(this_storage_path, "w")
        temp_file2.write("[\n\t\n]")
        temp_file2.close()
    this_storage_data = json.loads(open(this_storage_path, "r").read())

    # Calculate current time:
    now = datetime.now()

    # Main content:

    scraped = scrape_all_dirs(project_object["directories"], project_object["extensions"])
    print_good_info("Scraped!")
    to_store = {
        "time": str(now),
        "data": scraped
    }
    this_storage_data.append(to_store)

    return this_storage_data


def process_project(project_object : dict):

    # Find proper file for writing data
    this_storage_path = data_base_processor.find_last_temp_path(project_object)
    # if not os.path.exists(this_storage_path):
    #     temp_file2 = open(this_storage_path, "w")
    #     temp_file2.write("[\n\t\n]")
    #     temp_file2.close()
    # this_storage_data = json.loads(open(this_storage_path, "r").read())
    #
    # # Calculate current time:
    # now = datetime.now()
    #
    #
    # # Main content:
    #
    # scraped = scrape_all_dirs(project_object["directories"], project_object["extensions"])
    # print_good_info("Scraped:")
    # to_store = {
    #     "time" : str(now),
    #     "data" : scraped
    # }
    # this_storage_data.append(to_store)
    # print_as_json(to_store)

    this_storage_data = get_project_data(project_object)

    out_file = open(this_storage_path, "w")
    out_file.write(json.dumps(this_storage_data, indent=4, ensure_ascii=False))
    out_file.close()


def process_all_projects():
    for project in project_data:
        process_project(project)


process_all_projects()
