import os
from typing import*
from mylang import *
import collections
import itertools

def sub_strings(path : str, path0 : str):
    return path[len(path0):]


def get_file_data_with_extensions(base_path : str, extensions : List[str]) -> List[dict]:
    tree = os.walk(base_path)
    all_files = []
    for d, dirs, files in tree:
        for f in files:
            file_path = os.path.join(d, f)
            file_is_good = False
            for ext in extensions:
                if has_extension(f, ext):
                    file_is_good = True
                    break
            if not file_is_good:
                continue
            relative_path = sub_strings(file_path, base_path)
            if relative_path[0] == '\\':
                relative_path = relative_path[1:]
            all_files.append({"name": f, "absolute_path": file_path, "relative_path": relative_path})

    return all_files

def scrape_files(base_path : str, extensions : List[str]) -> List[dict]:
    """
    :returns: dict: for each filename there are:
            1) its length in lines,
            2) average non-blank line length,
            3) blank line number,
            4) number of symbols
            5) line length distribution
    """
    file_data = get_file_data_with_extensions(base_path, extensions)

    res = []
    for file in file_data:
        text = open(file["absolute_path"], "r", errors='ignore').read()
        lines = list(map(str.strip, text.splitlines()))
        real_lines = [l for l in lines if not is_spacieve(l)]
        line_lengths = [len(l) for l in lines]

        line_length_distribution = dict(collections.Counter(line_lengths))
        text_size = len(text)
        real_line_number = len(real_lines)
        all_line_number = len(lines)
        space_line_number = all_line_number - real_line_number

        file["line_length_distribution"] = line_length_distribution

        file["length"] = text_size

        file["blank_line_number"] = space_line_number
        file["non-blank_line_number"] = real_line_number

        file["line_number"] = all_line_number

        res.append(file)

    return res

def scrape_all_dirs(base_paths : List[str], extensions : List[str], debug = False) -> List[dict]:
    res = []
    for directory in base_paths:
        scraped = scrape_files(directory, extensions)
        if debug:
            print_good_info(f"This_scraped from {directory} with extensions {extensions}:")
            print(scraped)
        res.extend(scraped)

    return res



def counter(base_path : str, extensions : List[str], debug : bool = False) -> dict:
    total_sum = 0
    lines_sum = 0
    non_blank_lines_num = 0
    output = {}
    tree = os.walk(base_path)
    all_files = []
    for d, dirs, files in tree:
        for f in files:
            path = os.path.join(d, f)
            all_files.append(path)

    for file in all_files:
        good_file = False
        for extension in extensions:
            if file[-len(extension):] == extension:
                good_file = True
                break
        if not good_file:
            continue
        s = open(file, "r", encoding="utf-8").read()
        spl = s.split("\n")
        if debug:
            print(sub_strings(file, base_path), ":", len(s), "symbols, ", len(spl), "lines")
        total_sum += len(s)
        lines_sum += len(spl)
        for l in spl:
            if l != "":
                non_blank_lines_num += 1

    print("*********************")
    print("Total number of symbols in project:")
    print(total_sum)
    print("Total number of lines in project:")
    print(lines_sum)
    print("Average line length:")
    print(round(10 * total_sum / lines_sum) / 10)
    print("Average non-blank line length:")
    print(round(10 * total_sum / non_blank_lines_num) / 10)
    print("Percent of blank lines:")
    print(round(1000 * (1 - (non_blank_lines_num / lines_sum))) / 10, "%")

    output["Total number of symbols in project"] = total_sum
    output["Total number of lines in project"] = lines_sum
    output["Average line length"] = round(10 * total_sum / lines_sum) / 10
    return output


if __name__ == "__main__":

    string = json.dumps(scrape_files("D:\\Projects\\mylibs", [".cpp", ".py", ".h", ".hpp"]), indent = 4)
    print(string)
    open("test_project_stat.json", "w").write(string)

