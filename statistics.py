from startup import *
import data_base_processor
from mylang import *
from collections import defaultdict, Counter
from graphic_smoother import *

def count_total_project_size(project_stat : Dict) -> dict:
    return {
        "length" : sum([file["length"] for file in project_stat["data"] if not startswith(file["relative_path"], "venv")]),
        "lines" : sum([file["line_number"] for file in project_stat["data"] if not startswith(file["relative_path"], "venv")])
    }

def count_project_folder_stat(project_stat : Dict):
    # TODO!
    # +TODO: add new projects and change other project locations!

    folders = set()


    for file in project_stat["data"]:
        if startswith(file["relative_path"], "venv") or startswith(file["relative_path"], "cmake-build") or startswith(file["relative_path"], "."):
            continue

        splitted = split_if(file["relative_path"], lambda x: x == "/" or x == "\\")
        if len(splitted) == 1:
            # It`s a file, but not a folder!
            continue
        initial_folder = splitted[0]
        folders.add(initial_folder)

    cnt = defaultdict(int)
    for file in project_stat["data"]:
        if startswith(file["relative_path"], "venv") or startswith(file["relative_path"], "cmake-build") or startswith(
                file["relative_path"], "."):
            continue

        splitted = split_if(file["relative_path"], lambda x: x == "/" or x == "\\")
        if len(splitted) == 1:
            # It`s a file, but not a folder!
            continue
        initial_folder = splitted[0]


        cnt[initial_folder] = cnt[initial_folder] + file["length"]

    values = sorted([(cnt[i], i) for i in cnt])  # [::-1]
    print(values)

    fig, ax = plt.subplots()
    xs = np.arange(len(values))
    plt.bar(xs, [v[0] for v in values])

    plt.xticks(xs, tuple([v[1] for v in values]))
    plt.show()

def count_project_extension_stat(project_temp : Dict) -> Dict[str, defaultdict]:
    symb_res = defaultdict(int)
    for file in project_temp["data"]:
        symb_res[get_file_extension(file["name"])] += file["length"]

    line_res = defaultdict(int)
    for file in project_temp["data"]:
        line_res[get_file_extension(file["name"])] += file["line_number"]

    return { "lines" : line_res, "symbols" : symb_res }

def count_all_project_sizes(all_data : list):
    for proj in all_data:
        last_temp = data_base_processor.load_last_proj_temp(proj)
        print_good_info(f"Total project size data: {count_total_project_size(last_temp)} of project \"{proj['name']}\"")



def graph_all_file_line_length_distribution(all_projects):
    res_counter = Counter()
    for this_project_data in all_projects:
        project = data_base_processor.load_last_proj_temp(this_project_data)
        for file in project["data"]:
            this_counter = Counter(file["line_length_distribution"])
            res_counter += this_counter
    non_smoothed_graph = sorted([(int(k), res_counter[k]) for k in res_counter])
    print(non_smoothed_graph)
    smoothed_graph = smooth_graph_as_log(non_smoothed_graph, 0.1, 1000)
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_yscale('log')
    ax.set_xscale('log')
    plot_tuple_graph(ax, non_smoothed_graph)
    plot_tuple_graph(ax, smoothed_graph)
    plt.show()


def graph_file_extension_line_length_distribution(all_projects, extensions = (".py", ".cpp")):
    fig = plt.figure()
    ax = fig.add_subplot()


    ax.set_yscale('log')
    ax.set_xscale('log')

    for extension in extensions:
        res_counter = Counter()

        for this_project_data in all_projects:
            project = data_base_processor.load_last_proj_temp(this_project_data)
            for file in project["data"]:
                if has_extension(file["name"], extension) and not startswith(file["relative_path"], "venv"):
                    this_counter = Counter(file["line_length_distribution"])
                    res_counter += this_counter
        non_smoothed_graph = sorted([(int(k), res_counter[k]) for k in res_counter])
        print(non_smoothed_graph)
        smoothed_graph = smooth_graph_as_log(non_smoothed_graph, 0.1, 1000)
        ax.plot([i[0] for i in smoothed_graph], [i[1] for i in smoothed_graph], label=extension)

    ax.legend()
    plt.show()



if __name__ == "__main__":
    # TODO: delete useless (duplicated) logs
    # TODO: project history stats!!!
    count_project_folder_stat(data_base_processor.load_last_proj_temp(data_base_processor.select_project_by_name(project_data, "Pythonic")))
    # count_all_project_sizes(project_data)
    # print_as_json(count_project_extension_stat(data_base_processor.load_last_proj_temp(project_data[3])))
    # graph_all_file_line_length_distribution(project_data)
    # graph_file_extension_line_length_distribution(project_data)
