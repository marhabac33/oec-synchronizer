#!/usr/bin/python3
#
# Main program for Open Exoplanet Catalogue (OEC) synchronization extension.


import argparse
import datetime
import json
import logging
import os
import re
import sys
import tempfile
import urllib.request as req
from oec_sync_utils import *


def default(args, oec_main_path, config):
    ''' (Namespace, str, dict{str: obj}) -> None
    Print help instructions for program.
    '''
    exit(0)


def init(args, oec_main_path, config):
    ''' (Namespace, str, dict{str: obj}) -> None
    Initializes oec_sync program, saving all user inputted values.
    '''
    # Check for saved repo:
    repo_file = os.path.join(oec_main_path, REPO_FILE)
    if (os.path.isfile(repo_file)):
        print('ERROR: oec_sync.py must be destroyed before use new init can ' +
              'be set.\n' +
              '>>> ./oed_sync.py destroy')
        exit(1)

    user_data = vars(args)
    # Get origin data:
    origin_data = user_data['down'].split('/')
    if (len(origin_data) != 2):
        print('ERROR: invalid format downstream GitHub repository must be ' +
              'given as: owner/repo')
        exit(1)
    origin_owner = origin_data[0]
    origin_repo = origin_data[1]
    email = user_data['email']
    config[CLONED_REPO_NAME] = origin_repo
    # Get upstream data if given:
    if (('up' in user_data) and (not (user_data['up'] is None))):
        upstream_data = user_data['up'].split('/')
        if (len(upstream_data) != 2):
            print('ERROR: invalid format upstream GitHub repository must be ' +
                  'given as: owner/repo')
            exit(1)        
        upstream_owner = upstream_data[0]
        upstream_repo = upstream_data[1]
    else:
        upstream_owner = origin_owner
        upstream_repo = origin_repo
    # Get user input to generate oauth for GitHub account.
    os.system('curl -u ' + origin_owner + ' --data \'{"scopes":["repo"], ' +
              '"note":"oec_sync.py"}\'' + ' https://api.github.com/' +
              'authorizations > ' + OAUTH_FILE) 
    with open(OAUTH_FILE) as oauth_file:
        try:
            oauth_data = json.load(oauth_file)
            oauth = str(oauth_data['token'])
            oauth_id = str(oauth_data['id'])
        except:
            print('ERROR: oec_sync.py could not create oauth access token. ' +
                  'Check internet connection or oauth may already exist. ' +
                  'Log into ' + origin_repo + '/' + origin_repo + ' and ' +
                  'under settings>Personal access tokens delete the token ' +
                  'labeled oec_sync.py')
            exit(1) 
    os.system('rm ' + OAUTH_FILE)
    repo = GitRepo(oauth, oauth_id, origin_owner, origin_repo, upstream_owner,
                   upstream_repo)
    # Check that repo iniitalized properly.
    if (not repo.exists()):
        print('ERROR: creating GitHub Repo, check ' + origin_repo + '/' +
              origin_repo + ' values. Log into ' + origin_repo + '/' +
              origin_repo + ' and under settings>Personal access tokens ' +
              'delete the token labeled oec_sync.py and re-run init.')
        exit(1)
    # Update repo with lastest data from upstream GitHub repo, and verify
    # upstream repository.
    if (os.system("git pull 'https://github.com/" + upstream_owner + "/" +
                  upstream_repo + ".git' master") != 0):
        print('ERROR: updating GitHub repository from ' + upstream_owner +
              '/' + upstream_repo + '. Check that ' + origin_repo + '/' +
              origin_repo + ' is a fork of ' + upstream_owner +
              '/' + upstream_repo + '. Log into ' + origin_repo + '/' +
              origin_repo + ' and under settings>Personal access tokens ' +
              'delete the token labeled oec_sync.py and re-run init.')
        exit(1)
    # Configure repo credentials:
    os.system('git config user.name "' + origin_owner + '"')
    os.system('git config user.email "' + email + '"')    
    # Save repo file:
    save_gitrepo(repo, repo_file)
    # Save config file:
    config_file = os.path.join(oec_main_path, CONFIG_FILE)
    save_config(config, config_file)
    exit(0)


def run(args, oec_main_path, config):
    ''' (Namespace, str, dict{str: obj}) -> None
    Main OEC update program. Test version that uses subset of full OEC data
    set, in test_data folder.
    '''
    # Check for saved repo:
    repo_file = os.path.join(oec_main_path, REPO_FILE)
    if (not os.path.isfile(repo_file)):
        print('ERROR: oec_sync.py must be initalized before use.\n' +
              '>>> ./oed_sync.py init -d owner/repo -e email [-u owner/repo]')
        exit(1)

    # Set up file for logging:
    log_file = os.path.join(oec_main_path, LOG_FILE)
    logging.basicConfig(filename=log_file)

    # Create a temporary working directory for csv files.
    csv_dir = tempfile.TemporaryDirectory()

    # List to hold file path and name of downloaded csv files.
    csv_files = []
    # For each catalogue being monitored:
    for (file_name, url) in CATALOGUE_URLS:
        file_path = download_csv_file(url, (file_name + CSV_END), csv_dir.name)
        # If download was successful:
        if file_path:
            csv_files.append((file_path, file_name))

    # If no download was successful:    
    if not csv_files:
        logging.warning('Warning: No files downloaded on %s.',
                        str(datetime.datetime.now()))
        csv_dir.cleanup()
        exit(1)
    
    # Check if existing mapping of exoplanet to last update date exists.
    update_tracker_file = os.path.join(oec_main_path, UPDATE_TRACKER_FILE)  
    update_tracker = load_update_tracker(update_tracker_file)

    # Check if existing GitRepo saved object exists and a cloned repository is
    # saved in local directory.
    repo = load_gitrepo(repo_file)
    if ((repo is None) or (not repo.exists())):
        logging.exception('%s: GitHub repo failed to initalize',
                          str(datetime.datetime.now()))
        csv_dir.cleanup()
        exit(1)

    # Update repo with lastest data from upstream GitHub repo.
    repo.update()
    # Remove local and remote branches that have been merged/closed via pull
    # request since last run.
    repo.clean_branches()
    
    # Create a mapping dict(alias: xml sytem file):
    alias_to_xml = {}
    uniform_alias_to_xml = {}
    set_xml_aliases(os.path.join(os.getcwd(), SYSTEM_DIR), alias_to_xml,
                    uniform_alias_to_xml, repo)

    # For each csv file downloaded:
    for (file_path, file_name) in csv_files:

        # Iterable of dicts of column name to exoplanet row data.
        exoplanet_data = read_csv(file_path)
        # Dict mapping XML tags/attributes to column names.
        catalogue_map = CATALOGUE_TO_MAP[file_name]
        # Check if mapping is currently being tracked and get dict mapping
        # exoplanet names to last update dates:
        if (catalogue_map[MAPPING] in update_tracker):
            cat_updates = update_tracker[catalogue_map[MAPPING]]
        # If not being tracked then create new dict to track this catalogue:
        else:
            update_tracker[catalogue_map[MAPPING]] = {}
            cat_updates = update_tracker[catalogue_map[MAPPING]]

        # For each dict of exoplanet data:
        for exoplanet in exoplanet_data:
            (system_name, exoplanet_name, csv_update) = get_csv_identifiers(
                exoplanet, catalogue_map)
            # If no system or exoplanet name is given, cannot identify which
            # system/planet to update, skip and continue with next row.
            if ((system_name is None) or (exoplanet_name is None)):
                continue

            # Check if system name is one of the alias's in the existing
            # systemXML files. If yes use existing, else create new.
            validation_req = False
            uniform_system_name = re.sub(r'\W+|[_]+', '', system_name).lower()
            uniform_planet_name = re.sub(r'\W+|[_]+', '',
                                         exoplanet_name).lower()             
            # If the exoplanet name is on the redo list:
            if (exoplanet_name in repo.redo_planets()):
                if (system_name in alias_to_xml):
                    system_xml = alias_to_xml[system_name]
                elif (exoplanet_name in alias_to_xml):
                    system_xml = alias_to_xml[exoplanet_name]
                else:
                    system_xml = SystemXML(system_name + XML_END)
                    # Add xml alias and xml file to dict:
                    alias_to_xml[system_name] = system_xml
            else:               
                if (system_name in alias_to_xml):
                    system_xml = alias_to_xml[system_name]
                elif (exoplanet_name in alias_to_xml):
                    system_xml = alias_to_xml[exoplanet_name]
                # Check for possible typos/differences in formatting of aliases
                elif (uniform_system_name in uniform_alias_to_xml):
                    system_xml = uniform_alias_to_xml[uniform_system_name][0]
                    validation_req = True
                elif (uniform_planet_name in uniform_alias_to_xml):
                    system_xml = uniform_alias_to_xml[uniform_planet_name][0]
                    validation_req = True
                else:
                    system_xml = SystemXML(system_name + XML_END)
                    # Add xml alias and xml file to dict:
                    alias_to_xml[system_name] = system_xml

            # Get branch name for system.xml:
            branch = re.sub(r'\W+|[_]+', '', system_xml.name)
            # If the number of branches is at the given limit, stop checking
            # for updates on this run and begin issuing pull requests for
            # updated branches.
            if ((not (repo.branches() is None)) and
                (len(repo.branches()) > config[MAX_PULLS])):
                if (not (branch in repo.branches())):
                    continue

            # Check if the current exoplanet's last update is being tracked:
            if (exoplanet_name in repo.redo_planets()):
                repo.redo_planets().remove(exoplanet_name)
                cat_updates[exoplanet_name] = exoplanet
            elif (exoplanet_name in cat_updates):
                # If the exoplanet has not been updated since the last check,
                # then skip and continue with next exoplanet.
                if (cat_updates[exoplanet_name] == exoplanet):
                    continue
                # Else update to new csv date and continue xml update.
                else:
                    cat_updates[exoplanet_name] = exoplanet
            # Else set xml to track current planet, and compare csv date to xml
            # date.
            else:
                cat_updates[exoplanet_name] = exoplanet

            # Create new/updated XML file for given exoplanet data (only
            # returns Ture if data has actually changed, skips otherwise).
            if (new_system_xml(exoplanet, catalogue_map, system_xml,
                               system_name, config[TOLERANCE])):
                # If validation is required, then set different validation msg.
                orig_alias = None
                if (validation_req and
                    (uniform_system_name in uniform_alias_to_xml)):
                    orig_alias = uniform_alias_to_xml[uniform_system_name][1]
                    system_xml.add_validation_msg()
                elif (validation_req and
                      (uniform_planet_name in uniform_alias_to_xml)):
                    orig_alias = uniform_alias_to_xml[uniform_planet_name][1]
                    system_xml.add_validation_msg()
                # Check if branch for system.xml has been created:
                if (not repo.checkout(branch, validation_req)):
                    continue                
                system_path = os.path.join(os.getcwd(), SYSTEM_DIR)
                save_system_xml(system_xml, system_path)
                # Add and commit system_xml fill to git repo on current branch.
                repo.stage(system_xml, exoplanet_name, catalogue_map[SOURCE],
                           validation_req, orig_alias)
                # Add reference to pull messege.
                system_xml.add_references(exoplanet_name,
                                          catalogue_map[MAPPING])
                # Return to master branch.
                repo.checkout()

    # Issue pull request for each branch of current repo.
    repo.issue_pull_requests()
    # Save update tracker and GitRepo for next run
    save_update_tracker(update_tracker, update_tracker_file)
    save_gitrepo(repo, repo_file)
    # Change to repo parent directory.
    os.chdir(oec_main_path)
    # Delete downloaded csv files and directory.
    csv_dir.cleanup()
    exit(0)


def set_auto(args, oec_main_path, config):
    ''' (Namespace, str, dict{str: obj}) -> None
    Sets time of automatic runing of oec_sync.py and allows the user to turn
    automatic updating on and off, by given --on and --off command line
    arguments respectivly.
    '''
    # Check for saved repo:
    repo_file = os.path.join(oec_main_path, REPO_FILE)
    if (not os.path.isfile(repo_file)):
        print('ERROR: oec_sync.py must be initalized before use.\n' +
              '>>> ./oed_sync.py init -d owner/repo -e email [-u owner/repo]')
        exit(1)

    # If given set the hour and minute values in the config file:
    user_data = vars(args)
    if (('hour' in user_data) and (not (user_data['hour'] is None))):
        hour = user_data['hour']
        if ((0 <= hour ) and (hour < 24)):
            config[HOUR] = hour
        else:
            print('ERROR [--hour hour] Must be a value between 0-23.')
            exit(1)
    if (('minute' in user_data) and (not (user_data['minute'] is None))):
        minute = user_data['minute']
        if ((0 <= minute) and (minute < 59)):
            config[MINUTE] = minute
        else:
            print('ERROR [--minute minute] Must be a value between 0-59.')
            exit(1)

    # If given update the automatic updateing on/off state in the config file.
    on = user_data['on']
    off = user_data['off']
    if (on and off):
        print('ERROR can not select both --on and --off.')
        exit(1)
    elif (on):
        config[AUTO_STATE] = True
    elif (off):
        config[AUTO_STATE] = False

    # Save updates to the config file:
    save_config(config, os.path.join(oec_main_path, CONFIG_FILE))
    # Update/set cron job for program:
    if (not set_execution(oec_main_path, RUN_CMD, config[AUTO_STATE],
                          config[HOUR], config[MINUTE])):
        print('ERROR Failed to set automatic updating.')
        exit(1)   
    exit(0)


def destroy(args, oec_main_path, config):
    ''' (Namespace, str, dict{str: obj}) -> None
    Given empty Namespace and a string of the file path to the directory
    holding oec_sync.py, will delete any branches created by program,
    delete the local copy of the cloned repository, and the saved user
    information, saved GitHub repository metadat, and saved update tracking
    information. WARNING: Can not be undone, once destroyed oec_sync.py must
    be re-initialized before further use, all saved information is destroyed.
    Does not effect pull requests that have already been merged, or closed.
    '''
    # If saved repo is present, delete all branches and local cloned repo.
    if (os.path.isfile(os.path.join(oec_main_path, REPO_FILE))):
        repo = load_gitrepo(os.path.join(oec_main_path, REPO_FILE))
        if (not (repo is None)):
            repo.cleanup()
    if ((not (config[CLONED_REPO_NAME] is None)) and
         os.path.isdir(os.path.join(oec_main_path, config[CLONED_REPO_NAME]))):
        repo_path = os.path.join(oec_main_path, config[CLONED_REPO_NAME])
        os.system("rm -r '" + repo_path + "'")
    os.chdir(oec_main_path)
    # If present delete saved repo file:
    if (os.path.isfile(os.path.join(oec_main_path, REPO_FILE))):
        os.system('rm ' + os.path.join(oec_main_path, REPO_FILE))
    # If present delete saved update tracker file:
    if (os.path.isfile(os.path.join(oec_main_path, UPDATE_TRACKER_FILE))):
        os.system('rm ' + os.path.join(oec_main_path, UPDATE_TRACKER_FILE))
    # If present delete saved config file:
    if (os.path.isfile(os.path.join(oec_main_path, CONFIG_FILE))):
        os.system('rm ' + os.path.join(oec_main_path, CONFIG_FILE))
    exit(0)


if __name__ == '__main__':
    # For running crontab, change working directroy to scripts home directory:
    oec_main_path = sys.path[0]
    # Save directory path for OEC Synchronizer:
    os.chdir(oec_main_path)
    
    # Initialize configuration settings:
    config_file = os.path.join(oec_main_path, CONFIG_FILE)
    config = load_config(config_file)
    
    # Parse comand line arguments.
    parser = argparse.ArgumentParser(description=MAIN_DESCRIPTION)
    parser.set_defaults(func=default)
    parser.add_argument('-t', '--tolerance', type=float, dest=TOLERANCE,
                        help=TOLERANCE_HELP)
    parser.add_argument('-m', '--max-pulls', type=int, dest=MAX_PULLS,
                        help=MAX_PULLS_HELP)    
    subparsers = parser.add_subparsers()
    
    parser_init = subparsers.add_parser('init', help=INIT_HELP)
    parser_init.add_argument('-d', '--downstream', dest='down',
                             metavar='owner/repo', help=DOWNSTREAM_HELP,
                             required=True)
    parser_init.add_argument('-e', '--email', dest='email', metavar='email',
                             help=EMAIL_HELP, required=True)
    parser_init.add_argument('-u', '--upstream', dest='up',
                             metavar='owner/repo', help=UPSTREAM_HELP)
    parser_init.set_defaults(func=init)
    
    parser_run = subparsers.add_parser('run', help=RUN_HELP)
    parser_run.set_defaults(func=run)

    parser_set_auto = subparsers.add_parser('set-auto', help=SET_AUTO_HELP)
    parser_set_auto.add_argument('--hour', dest='hour',
                                 type=int, help=HOUR_HELP)
    parser_set_auto.add_argument('--minute', dest='minute',
                                 type=int, help=MINUTE_HELP)
    parser_set_auto.add_argument('--on', action='store_true', dest='on',
                                 help=ON_HELP)
    parser_set_auto.add_argument('--off', action='store_true', dest='off',
                                 help=OFF_HELP)
    parser_set_auto.set_defaults(func=set_auto)
    
    parser_destroy = subparsers.add_parser('destroy', help=DESTROY_HELP)
    parser_destroy.set_defaults(func=destroy)
    
    args = parser.parse_args()
    if ((TOLERANCE in vars(args)) and (not (vars(args)[TOLERANCE] is None))):
        tolerance_value = (vars(args)[TOLERANCE] / 100)
        if ((0 < tolerance_value) and (tolerance_value < 1)):
            config[TOLERANCE] = tolerance_value
        else:
            print('ERROR: [-t tolerance] must be a decimal numeric value ' +
                    'between 0 and 100.')
            exit(1)
        save_config(config, config_file)
        
    if ((MAX_PULLS in vars(args)) and (not (vars(args)[MAX_PULLS] is None))):
        max_pull_value = vars(args)[MAX_PULLS]
        if ((0 < max_pull_value) and (max_pull_value < 250)):
            config[MAX_PULLS] = max_pull_value
        else:
            print('ERROR: [-m max-pulls] must be an integer numeric value ' +
                    'between 0 and 250.')
            exit(1)
        save_config(config, config_file)

    args.func(args, oec_main_path, config)

