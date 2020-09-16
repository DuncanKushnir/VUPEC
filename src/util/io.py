import os

import util.locations as loc


def list_subfolders(path):
    """
    returns the subfolders of a given path
    :param path: a path
    :return: a list of folder item, full path tuples
    """
    return [(f.name, f.path) for f in os.scandir(path) if f.is_dir()]


def list_files(path, ext_whitelist=None):
    """
    returns the files in a given directory
    :param path: the path to search in
    :param ext_whitelist: the permissible extensions to return
    :return:
    """
    if ext_whitelist is not None and not isinstance(ext_whitelist, list):
        ext_whitelist = [ext_whitelist]

    return [
        (f.name, f.path)
        for f in os.scandir(path)
        if f.is_file()
        and ((not ext_whitelist) or os.path.splitext(f.name)[-1] in ext_whitelist)
    ]


def process_files(path, process_function, ext_whitelist=None):
    """
    calls process_function for every file (or all those with matching extensions)
    in a directory
    :param path: the path to process
    :param process_function: called with every path found
    :param ext_whitelist: an extention e.g. '.dat' or list of extensions to include
    :return: a {fname: function return dict} for each file
    """
    return {
        fname: process_function(fpath)
        for fname, fpath in list_files(path, ext_whitelist)
    }


def process_subdir_files(path, process_function, ext_whitelist=None):
    """
    :param path: the path in which all subdirectories will have their files processed
    :param process_function: called with every path found
    :param ext_whitelist: an extention e.g. '.dat' or list of extensions to include
    :return:
    """
    return {
        dname: process_files(dpath, process_function, ext_whitelist)
        for dname, dpath in list_subfolders(path)
    }


def grab_control_panel():
    """
    Gets the excel control panel for input
    :return: an openpyxl workbook
    """
    import openpyxl

    wb = openpyxl.load_workbook(loc.CTL_PANEL_FILE)
    return wb
