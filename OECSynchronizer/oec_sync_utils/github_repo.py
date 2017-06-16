#!/usr/bin/python3
#
# Contains classes, to be used for representing a GitHub repository.

import datetime
import json
import logging
import os
import tempfile
import urllib.request as req


class GitRepo(object):
    ''' Class used to represent a GitHub repository.'''

    def __init__(self, oauth, oauth_id, origin_user, origin_repo, up_user,
                 up_repo):
        ''' (self, str, str, str, str, str, str) -> None
        Clones the https GitHub repository from the given origin GitHub
        repository owned by given origin user, using given OAuth
        authentication. The given upstream repo owned by the given uptream user
        will be the GitHub repo to which pull requests are issued and update
        data is pulled from.
        '''
        # Save file path to the OEC program directory.
        self._init_dir = os.getcwd()
        if (os.system("git clone 'https://" + oauth + "@github.com/" +
                      origin_user + "/" + origin_repo + ".git'") == 0):
            self._exists = True
            self._oauth = oauth
            self._oauth_id = oauth_id
            self._origin_user = origin_user
            self._origin_repo = origin_repo
            self._up_user = up_user
            self._up_repo = up_repo
            # Set absolute file path on system to cloned repo.
            self._repo_path = os.path.join(os.getcwd(), self._origin_repo)
            # Change directories into cloned repo.
            os.chdir(self._repo_path)
            # Current branch.
            master = Branch('master')
            self._branch = master
            # List of branches
            self._branches = {str(master): master}
            self._validation_branches = []
            self._redo_planets = []
        else:
            self._exists = False
            logging.exception('%s: Failed to git clone %s/%s',
                              str(datetime.datetime.now()), origin_user,
                              origin_repo)

    def clone(self):
        ''' (self) -> bool
        Will clone a repo of the GitRepos settings to the init directory of the
        GitRepo. Returns True iff sucessful, else returns false. If sucessful
        will change into cloned repo directory.
        '''
        os.chdir(self._init_dir)
        if (os.system("git clone 'https://" + self._oauth + "@github.com/" +
                      self._origin_user + "/" + self._origin_repo + ".git'") ==
            0):
            # Set absolute file path on system to cloned repo.
            self._repo_path = os.path.join(os.getcwd(), self._origin_repo)
            # Change directories into cloned repo.
            os.chdir(self._repo_path)
            # Checkout master branch.
            self.checkout()
            self._branch = self._branches['master']
            return True
        else:
            self._exists = False
            logging.exception('%s: Failed to git clone %s/%s',
                              str(datetime.datetime.now()), self._origin_user,
                              self._origin_repo)
            return False

    def exists(self):
        ''' (self) -> bool
        Returns True iff the repo was created correctly.
        '''
        return self._exists

    def path(self):
        ''' (self) -> str
        Returns a string absolute file path to git repository head file.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return None
        return self._repo_path

    def redo_planets(self):
        ''' (self) -> list[str]
        Returns a list of planet names that need to be redone because they were
        for human verification and were rejected.
        '''
        return self._redo_planets

    def branches(self):
        ''' (self) -> dict{str: Branch}
        Returns dict of all branch names to Branch objects.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return None
        return self._branches

    def clean_branches(self):
        ''' (self) -> None
        Removes all local and remote branches that have been merged into
        upstream repository via pull request.
        '''
        # Get all open pull requests from upstream repo.
        open_pull_req = req.Request("https://api.github.com/repos/" +
                                    self._up_user + "/" + self._up_repo +
                                    "/pulls?per_page=300")
        response = req.urlopen(open_pull_req)
        raw_pulls = response.read().decode()
        open_pulls_json = json.loads(raw_pulls)
        response.close()
        open_pulls = set()
        del_branches = []
        # Get a set of open pull request numbers (how GitHub identifies
        # individual pull requests).
        for pull_req in open_pulls_json:
            open_pulls.add(str(pull_req['number']))
        # Check if each existing branch corrosponds to open pull request:
        for (b_name, branch) in self._branches.items():
            # If no pull request still exists for that branch, remove it:
            if ((b_name != 'master') and (not (branch.num() in open_pulls))):
                # Delete local branch.
                if (os.system("git branch -D '" + str(branch) + "'") != 0):
                    logging.exception('%s: git failed to delete local branch' +
                                      ' %s in repo %s',
                                      str(datetime.datetime.now()), b_name,
                                      self._repo_path)
                # Delete remote branch (may fail if remote branch already
                # deleted, fail here is acceptable).
                if (os.system("git push origin --delete -f '" + str(branch) +
                              "'") != 0):
                    logging.exception('%s: git failed to delete remote ' +
                                      'branch %s',
                                      str(datetime.datetime.now()), b_name)
                # Add branch to list of deleted branches.
                del_branches.append(b_name)
                # If branch required validation and was not merged, add to list
                # of xml files to redo:
                if (b_name in self._validation_branches):
                    try:
                        req.urlopen('https://api.github.com/repos/' +
                                    self._up_user + '/' + self._up_repo +
                                    '/pulls/' + branch.num() + '/merge')
                    except:
                        for planet_name in branch.updates():
                            self._redo_planets.append(planet_name)
                    # Remove branch from list of branches for validation.
                    self._validation_branches.remove(b_name)
        # Remove branch from self._branches (cannot modify dict while iter is
        # running above).
        for branch in del_branches:
            del self._branches[branch]
        # Reset tracking for each branch:
        for (b_name, branch) in self._branches.items():
            branch.set_xml(None)

    def update(self):
        ''' (self) -> bool
        Updates master branch of GitRepo to lastest version from upstream
        GitHub repository. Returns True iff successful, False otherwise logging
        error.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return False
        # Pull updates to local origin repo from upstream repo:
        if (os.system("git pull 'https://github.com/" + self._up_user + "/" +
                      self._up_repo + ".git' master") == 0):
            # Push updates from local origin repo to remote origin repo:
            if (os.system("git push origin master") == 0):
                return True
            else:
                logging.exception('%s: git push failed for %s',
                                  str(datetime.datetime.now()),
                                  self._repo_path)
                return False
        else:
            logging.exception('%s: git pull %s failed for %s',
                              str(datetime.datetime.now()), url,
                              self._repo_path)
            return False

    def checkout(self, branch=None, validation_req=False):
        ''' (self, str, bool) -> bool
        Given a string name of a branch, will git checkout into branch if it
        exists or create a new branch of that name and checkout that branch
        if it does not exist. If branch is not given, will checkout into
        master branch. Returns True iff successful, False otherwise logging
        error.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return False
        # If no branch is given checkout master branch:
        if not branch:
            if (os.system("git checkout master") == 0):
                self._branch = self._branches['master']
                return True
            else:
                logging.exception('%s: git checkout master for in repo %s',
                                  str(datetime.datetime.now()),
                                  self._repo_path)
                return False
            
        # If branch exists checkout.
        if (branch in self._branches):
            if (os.system("git checkout '" + branch + "'") == 0):
                self._branch = self._branches[branch]
                if (validation_req):
                    if (not (branch in self._validation_branches)):
                        self._validation_branches.append(branch)
                return True
            else:
                logging.exception('%s: git checkout failed for branch %s ' +
                                  'in repo %s', str(datetime.datetime.now()),
                                  branch, self._repo_path)
                return False
        # Otherwise create new branch with this name.
        else:
            if (os.system("git checkout -b '" + branch + "'") == 0):
                self._branches[branch] = Branch(branch)
                self._branch = self._branches[branch]
                if (validation_req):
                    if (not (branch in self._validation_branches)):
                        self._validation_branches.append(branch)
                return True
            else:
                logging.exception('%s: git creation and checkout failed for ' +
                                  'branch %s in repo %s',
                                  str(datetime.datetime.now()), branch,
                                  self._repo_path)
                return False

    def stage(self, system_xml, exoplanet_name, source=None,
              validation_req=False, original_alias=None):
        ''' (self, SystemXML, str, str, bool, str) -> bool
        Given a SystemXML object, will stage (git add and git commit) the
        file that the SystemXML represents on the current branch. Includes
        source in commit message if given. Returns True if successful, False
        otherwise logging error.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return False
        # Add xml_file to git staging (git add then git commit with mesg):
        if (os.system("git add '" + system_xml.file_path + "'") == 0):
            if (os.system("git commit -m '" +
                          system_xml.commit_msg(exoplanet_name, source,
                                                validation_req,
                                                original_alias) +
                          "'") == 0):
                self._branch.set_xml(system_xml)
                self._branch.add_update(exoplanet_name)
                return True
            else:
                logging.exception('%s: git commit failed for %s in branch %s' +
                                  'in repo %s', str(datetime.datetime.now()),
                                  system_xml.file_path, str(self._branch),
                                  self._repo_path)
                return False
        else:
            logging.exception('%s: git add failed for %s in branch %s in' +
                              ' repo %s', str(datetime.datetime.now()),
                              system_xml.file_path, str(self._branch),
                              self._repo_path)
            return False

    def issue_pull_requests(self):
        ''' (self) -> None
        Pushes all branches to origin (forked OEC repository), then creates
        and issues a pull request for each branch to the upstream OEC GitHub
        repositiory set in the CONFIG section of the constants. Logs any errors
        that occure.
        '''
        if (not self._exists):
            logging.exception('%s: GitRepo failed to initalize',
                              str(datetime.datetime.now()))
            return None
        # Ensure master branch is checked out.
        if (str(self._branch) != 'master'):
            self.checkout()
        # For each branch
        for (b_name, branch) in self._branches.items():
            # If this branch has not been updated, skip issuing pull request.
            if (branch.xml() is None):
                continue
            # Push branch to forked OEC repo.
            if (os.system("git push origin '" + b_name + "'") == 0):
                title = branch.xml().pull_title()
                msg = branch.xml().pull_msg()
                raw_req_data = {"title": title, "body": msg, "head":
                            (self._origin_user + ":" + b_name),
                             "base": "master"}
                req_data = json.dumps(raw_req_data).encode('utf8')
                # If branch has no existing pull request create new one:
                if (branch.num() is None):
                    pull_req = req.Request("https://api.github.com/repos/" +
                                           self._up_user + "/" +
                                           self._up_repo + "/pulls")
                # Else update existing pull request:
                else:
                    pull_req = req.Request("https://api.github.com/repos/" +
                                           self._up_user + "/" +
                                           self._up_repo + "/pulls/" +
                                           branch.num())                    
                pull_req.add_header('Authorization', 'token ' + self._oauth)
                pull_req.add_header('Accept', 'application/vnd.github.v3+json')
                try:
                    response = req.urlopen(pull_req, data=req_data)
                    raw_pull_data = response.read().decode()
                    pull_data = json.loads(raw_pull_data)
                    branch.set_num(str(pull_data['number']))
                except:
                    logging.exception('%s: pull failed to issue pull request' +
                                      ' from %s to %s',
                                      str(datetime.datetime.now()), b_name,
                                      (self._up_user + "/" + self._up_repo))
            else:
                logging.exception('%s: git failed to push to origin branch ' +
                                  '%s in repo %s',
                                  str(datetime.datetime.now()), b_name,
                                  self._up_repo)

    def cleanup(self):
        ''' (self) -> None
        Will delete any branches created by program, the remote oauth token,
        and delete the local copy of the cloned repository.
        '''
        for (b_name, branch) in self._branches.items():
            if (b_name != 'master'):
                # Does not check for remote or local branches existance,
                # ok if fails on individual branch, does not effect running
                # of destroy function.
                os.system("git branch -D '" + str(branch) + "'")
                os.system("git push origin --delete -f '" + str(branch) + "'")
        os.system('curl -u ' + self._origin_user + ' -X "DELETE" ' +
                  'https://api.github.com/authorizations/' + self._oauth_id)
        os.chdir(self._init_dir)
        os.system("rm -r '" + self._repo_path + "'")


class Branch(object):
    ''' Represents a branch of a GitHub repository.'''

    def __init__(self, name):
        ''' (self, str) -> None
        Creates and initializes a new branch object of given name.
        '''
        self._name = name
        self._num = None
        self._xml = None
        self._updated = []
    
    def __str__(self):
        ''' (self) -> str
        Returns a the name of the branch as a string.
        '''
        return self._name

    def set_num(self, num):
        ''' (self, str) -> None
        Sets the number of the pull request linked to this branch.
        '''
        self._num = num

    def num(self):
        ''' (self) -> str
        Returns the number of the pull request linked to this branch.
        '''
        return self._num

    def set_xml(self, xml):
        ''' (self, SystemXML) -> None
        Adds given SystemXML object to the branch.
        '''
        self._xml = xml

    def add_update(self, planet):
        ''' (self, str) -> None
        Adds given planet name to list of updated planets on branch.
        '''
        self._updated.append(planet)

    def xml(self):
        ''' (self) -> SystemXML
        Returns a the SystemXML file modified or created on this branch.
        '''
        return self._xml

    def updates(self):
        ''' (self) -> list[str]
        Returns a list of exoplanets modified or created on this branch.
        '''
        return self._updated

