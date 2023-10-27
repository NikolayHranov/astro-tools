import glob
import re
import os

main_path = "C:/Users/Nikolay/Desktop/New folder"


def distribute(path, filter):
    folder_path = f"{main_path}/images/{path}"
    file_pattern = "*_*s_*"
    files = glob.glob(os.path.join(folder_path, file_pattern))
    print(files)

    value_pattern = r"_(\d+)s_"

    values = []

    for file in files:
        match_ = re.search(value_pattern, file)
        if match_:
            second_star_value = match_.group(1)
            values.append(second_star_value)

    file_distribution = {}

    for value in values:
        pattern = f"*_{filter}_*_{value}s_*"
        file_distribution[value] = glob.glob(os.path.join(folder_path, pattern))

    return file_distribution
