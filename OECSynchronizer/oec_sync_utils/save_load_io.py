#!/usr/bin/python3
#
# Contains functions used to load and save date.


import datetime
import logging
import os
import pickle
from oec_sync_utils.constants import *
from oec_sync_utils.github_repo import *


def load_gitrepo(repo_file_path):
    ''' (str) -> GitRepo
    Given an file path to a pickled (saved) GitRepo object, will attempt to
    load the GitRepo and change into cloned directory. If cloned directory is
    not present or lacks git tree, will delete directory (if present) and clone
    repo. If no pickled GitRepo at given location or error occures will return
    None.
    '''
    if (os.path.isfile(repo_file_path)):
        try:
            with open(repo_file_path, 'rb') as repo_file:
                # Load repo from existing saved GitRepo object.
                repo = pickle.load(repo_file)
                # If cloned repo exists change into cloned repo.
                if os.path.isdir(os.path.join(repo.path(), ".git")):
                    # Change directories into cloned repo.
                    os.chdir(repo.path())
                # If the cloned repo directory exists but is not initialized,
                # remove directory and reclone repo.
                elif os.path.isdir(repo.path()):
                    os.system("rm -r '" + repo.path() + "'")
                    repo.clone()
                # If the cloned repo directory doesn't exist, clone directory
                # and change into newly cloned directory.
                else:
                    repo.clone()
                return repo
        except:
            logging.exception('%s: Saved GitHub repo failed to open',
                              str(datetime.datetime.now()))
            return None
    else:
        return None


def load_update_tracker(update_tracker_path):
    ''' (str) -> dict{str: dict{str: str}}
    Given an file path to a pickled (saved) dict that maps each catalogue name
    to a dict mapping each exoplanet name in that catalogue to the last update
    date for that exoplanet the last time the program was run. Returns empty
    dict if error or no file is present at given location.
    '''
    if (os.path.isfile(update_tracker_path)):
        try:
            with open(update_tracker_path, 'rb') as update_tracker_file:
                # Load update tracker from existing saved update tracking file.
                update_tracker = pickle.load(update_tracker_file)
                return update_tracker
        except:
            logging.exception('%s: Saved update tracking dict failed to open',
                              str(datetime.datetime.now()))
            return {}
    # Else create new empty one.
    else:
        return {}


def load_config(config_path):
    ''' (str) -> dict{str: obj}
    Given an file path to a pickled (saved) dict holding configuration
    settings. Returns empty dict if error or no file is present at given
    location.
    '''
    if (os.path.isfile(config_path)):
        try:
            with open(config_path, 'rb') as config_file:
                # Load config from existing saved config file.
                config = pickle.load(config_file)
                return config
        except:
            logging.exception('%s: Saved configuration dict failed to open',
                              str(datetime.datetime.now()))
            return DEFAULT_CONFIG
    # Else create new empty one.
    else:
        return DEFAULT_CONFIG


def save_update_tracker(update_tracker, update_tracker_path):
    ''' (dict{str: dict{str: str}}, str) -> None
    Saves given update tracker dict to given file path location.
    '''
    try:
        with open(update_tracker_path, 'wb') as update_tracker_file:
            # Save update tracker to UPDATE_TRACKER_FILE for next run.
            pickle.dump(update_tracker, update_tracker_file,
                        pickle.HIGHEST_PROTOCOL)
    except:
        logging.exception('%s: Update tracking failed to save',
                          str(datetime.datetime.now()))


def save_gitrepo(repo, repo_path):
    ''' (GitRepo, str) -> None
    Saves given GitRepo object to given file path location.
    '''
    try:
        with open(repo_path, 'wb') as repo_file:
            # Save repo to REPO_FILE for next run.
            pickle.dump(repo, repo_file, pickle.HIGHEST_PROTOCOL)
    except:
        logging.exception('%s: GitHub repo failed to save',
                          str(datetime.datetime.now()))


def save_config(config, config_path):
    ''' (dict{str, obj}, str) -> None
    Saves given configuration dict to given file path location.
    '''
    try:
        with open(config_path, 'wb') as config_file:
            # Save config to CONFIG_FILE for next run.
            pickle.dump(config, config_file, pickle.HIGHEST_PROTOCOL)
    except:
        logging.exception('%s: GitHub repo failed to save',
                          str(datetime.datetime.now()))


def save_system_xml(system_xml, system_path):
    ''' (str, str) -> bool
    Saves the given SystemXML file as a properly formated xml file. Returns
    True iff successful. Logs error message in event of failure.
    '''
    # Pretty print the xml.
    xml_file = str(system_xml)
    
    # Create file path for new/updated system.xml file.
    file_path = os.path.normpath(os.path.join(system_path,
                                              system_xml.file_name))
    system_xml.file_path = file_path
    try:
        with open(file_path, "w") as file:
            file.write(xml_file)
    except:
        logging.exception('%s: Could not open %s for writing.',
                          str(datetime.datetime.now()), file_path)
