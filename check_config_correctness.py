from startup import *

print_props("______________________________________________________________", console_color.CYAN, console_color.BOLD)

print("Checking directories:")

for project in project_data:
    good_flag = True
    for directory in project["directories"]:
        if not os.path.exists(directory):
            print_red(fr"Bad directory: {directory} from project: {project['name']}:")
            good_flag = False
    if good_flag:
        print_good_info(f"Successfully checked project directories: {project['name']}")


