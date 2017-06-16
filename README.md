# team05-Project Version 1.0 Open Exoplanet Catalogue (OEC) Synchronization Project (oec_sync)
Project created for team05

team05 members: ([Ian Ferguson](https://github.com/Mr-Ian-Ferguson), [Marhababanu Chariwala](https://github.com/marhabac33), [Ahsan Zia](https://github.com/ziaahsan), [Jubin Patel](https://github.com/PatelJubin), [Mu Xi (Lucy) Xing](https://github.com/LucyXMX)

This is repo for the CSCC01 project for team 05 (E.T).

This program generates automatic updates of system XML documents for the Open
Exoplanet Catalogue (OEC). Currently it only supports monitoring updates from:
http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=* and http://exoplanet.eu/catalog/csv.

WARNING INITIAL RUN (MANUAL OR AUTOMATIC) WILL GENERATE A LARGE NUMBER OF PULL REQUESTS

###Dependencies (MANDATORY):

If using Debian-based distributions like Ubuntu first run: >>> sudo apt-get update

1. A github (https://github.com/) account; either the OEC repository (https://github.com/openexoplanetcatalogue/open_exoplanet_catalogue/) or an account capable of forking the OEC repository.
    * For tutorial on using github: https://help.github.com/articles/good-resources-for-learning-git-and-github/

2. Python3 (https://www.python.org/):
   * For Debian-based distributions like Ubuntu, try apt-get: >>> sudo apt-get install python3
   * OR to install from Source:
        * Source download latest Python 3.x version available from: https://www.python.org/downloads/
        * Follow documentation instructions for your system.

3. git (https://git-scm.com/):
   * For Debian-based distributions like Ubuntu, try apt-get: >>> sudo apt-get install git
   * See: http://git-scm.com/download/linux for other flavours of Unix.
   * OR to install from Source:
        * To install Git from source, you need to have the following libraries that Git depends on: curl, zlib, openssl, expat, and libiconv.
        * See: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git for instructions.

4. curl (https://curl.haxx.se/):
   * For Debian-based distributions like Ubuntu, try apt-get: >>> sudo apt-get install curl

5. python3-crontab (https://pypi.python.org/pypi/python-crontab)
   * For Debian-based distributions like Ubuntu, try apt-get: >>> sudo apt-get install python3-crontab
   * OR (via pip)
   * For Debian-based distributions like Ubuntu, try apt-get: >>> sudo apt-get install python3-pip
   * Then >>> pip3 install python-crontab

###HELP/MAN Pages:
To see command line help documentation:
   * From Linux terminal run: >>> ./oec_demo.py -h
   * OR
   * From Linux terminal run: >>> ./oec_sync.py -h

To see command specific documentation:
   * From Linux terminal run: >>> ./oec_demo.py [command] -h
   * OR
   * From Linux terminal run: >>> ./oec_sync.py [command] -h

###SETUP:
Program must be initialized before first use, and/or adjustment of settings:

1. Install all needed dependencies (see above).

2. Navigate to [team05-Project/OECSynchronizer/](team05-Project/OECSynchronizer/) folder.

3. TO INITALIZE PROGRAM
   * The main program can be set up in two configurations:
   * 1) If no upstream Github repository is given then for each updated system xml file, a new branch will be created on the downstream repository and a pull request will be issued for each branch to the downstream repository. Note: in this configuration downstream repository must be the OEC repository (https://github.com/openexoplanetcatalogue/open_exoplanet_catalogue/) or a fork of the OEC repository, and email must be the email associated with the downstream Github repository.
       * From Linux terminal run: >>> ./oec_sync.py init -d downstream_repo_owner/downstream_repo_name  -e email_address
       * Note: init command will require Github password to generate oauth token for program (password is never stored).

   * 2) If upstream Github repository is given then for each updated system xml file, a new branch will be created on the downstream repository and a pull request will be issued for each branch to the upstream repository. Note: in this configuration upstream repository must be the OEC repository (https://github.com/openexoplanetcatalogue/open_exoplanet_catalogue/) or a fork of the OEC repository, downstream must be a fork of the upstream repository, and email must be the email associated with the downstream Github repository.
       * From Linux terminal run: >>> ./oec_sync.py init -d downstream_repo_owner/downstream_repo_name  -e email_address -u upstream_repo_owner/upstream_repo_name
       * Note: init command will require Github password to generate oauth token for program (password is never stored).

    * WARNING: Do not run the init for both oec_demo.py and oec_sync.py. Once run the init will apply to both programs as will the destroy command.

Setup complete!


###Running Program:
TO MANUALLY RUN DEMO PROGRAM (RECOMENDED FOR TESTING, ONLY USES SUBSET OF FULL NASA AND EXOPLANET.EU CATALOGUES)
 * Navigate to [team05-Project/OECSynchronizer/](team05-Project/OECSynchronizer/) folder.
 * From Linux terminal/shell run >>> ./oec_demo.py run
 * Note: Program must be run from command line.

OR

TO MANUALLY RUN MAIN PROGRAM (WARNING GENERATES LARGE NUMBER OF PULL REQUESTS ON INITIAL RUN)
 * Navigate to [team05-Project/OECSynchronizer/](team05-Project/OECSynchronizer/) folder.
 * From Linux terminal/shell run >>> ./oec_sync.py run
 * Note: Program must be run from command line.


###Setting Automatic Updating:
By default automatic updating is set to off, and to update at 12:00 am.

To turn automatic updating on:
   * From Linux terminal/shell run >>> ./oec_sync.py set-auto --on

To turn automatic updating off:
   * From Linux terminal/shell run >>> ./oec_sync.py set-auto --off

To set the hour when automatic updating will run (defaults to 0). Does not change off/on state:
   * From Linux terminal/shell run >>> ./oec_sync.py set-auto --hour (int between 0-23)

To set the minutes after the set hour when automatic updating will run (defaults to 0). Does not change off/on state:
   * From Linux terminal/shell run >>> ./oec_sync.py set-auto --minute (int between 0-59)


###Set Update Tolerance Level:
By default the tolerance level is set to 0 (i.e. all differences are cause for update regardless of size. The tolerance level is a decimal (float) percentage value below which changes are ignored in numeric values (note setting tolerance level does not effect inclusion of string/text values in updates). i.e. if set at 2.5% then any numeric values that has changed by less then 2.5% will not be updated (if that is the only difference in the xml file then no update/branch/pull request will be generated for that file). Note changes to the tolerance level will be applied to all future runs of the program until changed.

To set the tolerance level (defaults to 0):
   * From Linux terminal/shell run >>> ./oec_sync.py -t (float between 0-100)

###Set Maximum Number of Open Pull Requests (and associated branches):
By default the maximum number of open pull requests is set to 100. The maximum number of pulls is an integer value between 0-250. Any updates that would generate pull requests beyond the maximum pull limit will be put off until future runs of the program and the number of open pull requests is below the set limit. If set to a lower value then the current number of pull requests, no existing pull requests will be removed and no new pull requests will be generated until the number of open pull requests is below the current max-pull limit. Note changes to the maximum pulls limit will be applied to all future runs of the program until changed.

To set the max-pulls level (defaults to 100):
   * From Linux terminal/shell run >>> ./oec_sync.py -m (int between 0-250)

###Destroy Settings/Updates:
To remove init settings and any unmerged branches/pull requests:
   * From Linux terminal/shell run >>> ./oec_sync.py destroy
   * Note: destroy command will require Github password to destroy oauth token generated for program.



###Deliverable 1 files location:

1. Team Introduction:
  * content: Introduction of team and team members
  * location: [documents/deliverable1/E.T.pdf](./documents/deliverable1/E.T.pdf)

2. Team Agreement:
  * content: team's agree expectations and guideline
  * location: [documents/deliverable1/teamAgreement.pdf](./documents/deliverable1/teamAgreement.pdf)

###Deliverable 2 file location:

1. Persona and User Stories:
  * content: Persona and multiple user stories for the project.
  * location: [documents/deliverable2/PersonaAndUserStories.pdf](./documents/deliverable2/PersonaAndUserStories.pdf)

###Deliverable 3 file location:

1. Project Management:
  * content: Productive environment, product backlog, sprint backlog, release plan and Snapshots.
  * location: [documents/deliverable3/ProjectManagement.pdf](./documents/deliverable3/ProjectManagement.pdf)

###Deliverable 3 (Part 2) file location:

1. High Level System Design:
  * content: Diagram that represent component of the system, their role and their interaction.
  * location: [documents/deliverable3/HighLevelSystemDesign.pdf](./documents/deliverable3/HighLevelSystemDesign.pdf)

2. First Sprint Report:
  * content: Sprint backlog with tasks of each user stories, sprint overview and snapshot of task board and burndown chart
  * location: [documents/deliverable3/FristSprintReport.pdf](./documents/deliverable3/FristSprintReport.pdf)

3. MAIN PROGRAM:
  * location: [team05-Project/OECSynchronizer/oec_synchronizer.py](./OECSynchronizer/oec_synchronizer.py)
  * python script, run in linux/unix environment.
  * To run from terminal 1) navigate to folder, 2) ./oec_synchronizer.py (no command line arguments)
  * Expected results: will create (if not already created) two directories: cache and systems,
    cache will hold two downloaded csv files from <http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets>
    and <http://exoplanet.eu/catalog/csv>. Second systems folder will hold one properly formatted XML system file
    in OEC format (using same XML tags) for each star in the two csv folders. At this point in development
    some measurements will be wrong (conversions have not been implemented) and each system will contain only
    a single planet (updating existing XML files has not been implemented yet). Some mappings are still uncertain
    as well (if valid mappings exist) so some feilds may be blank that will be filled in in later sprints.

4. oec_sync_utils Package
  * location: [team05-Project/OECSynchronizer/oec_sync_utils](./OECSynchronizer/oec_sync_utils)
  * Not intended to be called directly.
  * Contains main functions used by oec_synchronizer.py
  * __init__.py (contains package info for oec_sync_utils)
  * constants.py (contains all constants, urls for csv files, file paths to cache and system folders, and
    mappings from XML tags to csv column headers for each catalogue used to generate exoplanet data).
  * csv_downloader.py (contains functions to download and save csv files from url).
  * csv_reader.py (contains functions to read csv files and extract data in usable formate).
  * xml_generator.py (contains functions to generate new XML OEC system pages given valid formated data
    from csv_reader.py and mappings from constants.py).

###Deliverable 4 files location:

1. Deliverable4Overview:
  * content: Additional Persona, Updated product backlog, updated release plan, Evidence of system validation and deliverable 4 overview.
  * location: [documents/deliverable3/Deliverable4Overview.pdf](./documents/deliverable4/Deliverable4Overview.pdf)

2. UpdatedHighLevelSystemDesign
  * content: Updated high level system design.
  * location: [documents/deliverable3/UpdatedHighLevelSystemDesign.pdf](./documents/deliverable4/UpdatedHighLevelSystemDesign.pdf)

3. CodeInspection:
  * content: Sprint backlog with tasks of each user stories, sprint overview and snapshot of task board and burndown chart
  * location: [documents/deliverable4/CodeInspection.pdf](./documents/deliverable4/CodeInspection.pdf)

4. Sprint2Report
  * content: Sprint 2 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable4/Sprint2Report.pdf](./documents/deliverable4/Sprint2Report.pdf)

5. Sprint3Report:
  * content: Sprint 3 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable4/Sprint3Report.pdf](./documents/deliverable4/Sprint3Report.pdf)

6. Sprint4Report:
  * content: Sprint 4 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable4/Sprint4Report.pdf](./documents/deliverable4/Sprint4Report.pdf)

7. Link to [Code Inspection Meeting Video](https://www.youtube.com/watch?v=tmOooxXFnhM)

###Deliverable 5 files location:

1. Deliverable5Overview:
  * content: Additional Persona, Updated product backlog, updated release plan, Evidence of system validation and deliverable 5 overview.
  * location: [documents/deliverable5/Deliverable5Overview.pdf](./documents/deliverable5/Deliverable5Overview.pdf)

2. UpdatedHighLevelSystemDesign
  * content: Updated high level system design.
  * location: [documents/deliverable5/HighLevelSystemDesign.pdf](./documents/deliverable5/HighLevelSystemDesign.pdf)

3. CodeInspection:
  * content: Sprint backlog with tasks of each user stories, sprint overview and snapshot of task board and burndown chart
  * location: [documents/deliverable5/CodeInspection.pdf](./documents/deliverable5/CodeInspection.pdf)

4. Sprint5Report
  * content: Sprint 5 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable5/Sprint5Report.pdf](./documents/deliverable5/Sprint5Report.pdf)

5. Sprint6Report:
  * content: Sprint 6 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable5/Sprint6Report.pdf](./documents/deliverable5/Sprint6Report.pdf)

6. Sprint7Report:
  * content: Sprint 7 backlog with task, snapshot of task board and burn down chart
  * location: [documents/deliverable5/Sprint7Report.pdf](./documents/deliverable5/Sprint7Report.pdf)

7. Link to [Code Inspection Meeting video (D5)](https://www.youtube.com/watch?v=NkPDU0voH64)
