from pathlib import Path


def find_all_cfg_files(dir_for_files):
    print(f"Directory to check for Macros is: {dir_for_files}")
    cfg_files = Path(dir_for_files).glob('**/*')
    config_file_list = []
    non_config_file_name_list = []
    for a_file in cfg_files:
        file_info = {
            "path_object": a_file,
            "name": a_file.name,
            "line_count": -1,
        }
        if ".cfg" in str(a_file):
            config_file_list.append(file_info)
        else:
            non_config_file_name_list.append(file_info)
    return config_file_list
