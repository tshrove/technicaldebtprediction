from configs import ConfigFactory
from classes import ProjectEventList
from classes import JIRAWrapper
from classes import MySQLExport
from classes import GitHubWrapper
from classes import StarGazer
from classes import DerivativeData
from datetime import datetime
import plotly.graph_objs as go
import plotly as py
from dateutil.parser import parse
import numpy as np


_project_id = 0
_num_of_bins = 25
config = ConfigFactory.factory()
dbe = MySQLExport(database='phd', username='root', password='mts0619', host='localhost')


def main():
    menu()


def technicaldebtbyproject_menu():
    _plot = input("How would you like to plot the project by [(1) date or (2) percentage): ")
    _key = input("Enter a project key (ex. OPT): ")
    _bins = input("How many bins would you like to limit the project to (ex. 10): ")
    _issuetypes = input("What issuestypes do you wish to collect (ex. Bug): ")
    ###
    # ToDo add input for start and end date
    if _plot == "":
        _plot = "percentage"
    else:
        if _plot == "1":
            _plot = "date"
        elif _plot == "2":
            _plot = "percentage"

    if _bins == "":
        _bins = None
    if _issuetypes == "":
        _issuetypes = config.get_issuetypes()[0]
    " for now get the project from the config file "
    _projects = config.get_projects()
    _filtered_projects = [p for p in _projects if p['key'] == _key]
    if len(_filtered_projects) > 0:
        _project = _filtered_projects[0]
        plot_by_project_bins(_project, _bins, _issuetypes, by=_plot)


def exportdebttodatabase_menu():
    _key = input("Enter a project key (ex. OPT or 'all' for all projects): ")
    #_bins = input("How many bins would you like to limit the project to (ex. 10): ")
    _issuetypes = input("What issuestypes do you wish to collect (ex. Bug): ")
    ###
    # ToDo add input for start and end date

    # if _bins == "":
    #     _bins = None
    if _issuetypes == "":
        _issuetypes = config.get_issuetypes()[0]
    " for now get the project from the config file "
    _projects = config.get_projects()
    if _key == 'all':
        for _project in _projects:
            export_data_to_db(project=_project, issuetypes=_issuetypes)
    else:
        _filtered_projects = [p for p in _projects if p['key'] == _key]
        if len(_filtered_projects) > 0:
            _project = _filtered_projects[0]
            export_data_to_db(project=_project, issuetypes=_issuetypes)


def projectstats_menu():
    _projects = config.get_projects()
    project_stats = []
    for project in _projects:
        _start_date = project['start_date']
        _end_date = project['end_date']
        if type(_start_date) is str:
            start = parse(_start_date)
        if type(_end_date) is str:
            end = parse(_end_date)
        _total_days = abs((end - start).days)
        project_stats.append(_total_days)

    projArr = np.array(project_stats)

    print('')
    print('Total Days: ' + str(sum(project_stats)))
    print('Total Projects ' + str(len(project_stats)))
    print('Mean (Days): ' + str(np.mean(projArr)))
    print('Mean (Years): ' + str(np.mean(projArr) / 365))
    print('Std Deviation (Days): ' + str(np.std(projArr)))
    print('Shortest Project (Days): ' + str(np.min(projArr)))
    print('Longest Project (Days): ' + str(np.max(projArr)))
    print('')


def github_stats_menu():
    dbe.open()
    _repo = input("What is the name of the repository?: ")
    _github = GitHubWrapper(username="tshrove@gmail.com", password="v2LUQeb4mKB4", repo=_repo)
    _stars_list = _github.get_stargazers()
    print("Total Count: " + _stars_list.totalCount)


def github_export_menu():
    dbe.open()
    # Delete everything before beginning
    dbe.deletestardata()
    _projects = config.get_projects()
    for project in _projects:
        _repo = project['github']
        print('importing github repo: ' + _repo)
        _github = GitHubWrapper(username="tshrove@gmail.com", password="v2LUQeb4mKB4", repo=_repo)
        _stars_list = _github.get_stargazers()
        dbe.export_stardata(star_list=_stars_list, repokey=_repo)


def github_normalize_menu():
    dbe.open()
    _projects = config.get_projects()
    for project in _projects:
        _repo = project['github']
        print('normalizing database star repo: ' + _repo)
        star_list = dbe.import_stardata(_repo)
        star_list = StarGazer.normalize(star_list=star_list,
                                        start_date=project['start_date'],
                                        end_date=datetime.now())
        ''' Update the data in the database. '''
        for star in star_list:
            dbe.update_star(star_id=star.id, star=star)


def derivative_of_stardata_menu():
    dbe.open()
    _projects = config.get_projects()
    for project in _projects:
        _repo = project['github']
        print('normalizing database star repo: ' + _repo)
        star_list = dbe.import_stardata(_repo)
        for i, val in enumerate(star_list[:-1]):
            _y = star_list[i+1].cumlative_value - star_list[i].cumlative_value
            _x = star_list[i+1].normalized_percentage - star_list[i].normalized_percentage
            ''' divisible by zero catch '''
            if _x == 0.0:
                _dydx = 0.0
            else:
                _dydx = _y/_x
            star_list[i].derivative_value_temp = _dydx
        # set the last value
        star_list[-1].derivative_value_temp = star_list[-2].derivative_value

        print('updating database with derivative data for star repo: ' + _repo)
        ''' Update the data in the database. '''
        for star in star_list:
            dbe.update_star(star_id=star.id, star=star)


def derivative_of_tddata_menu():
    dbe.open()
    _projects = config.get_projects()
    for project in _projects:
        _projectkey = project['key']
        print('normalizing data td project: ' + _projectkey)
        projecttd_list = dbe.import_tddata(_projectkey)
        for i, val in enumerate(projecttd_list[:-1]):
            _y = projecttd_list[i+1].cumlative_value - projecttd_list[i].cumlative_value
            _x = projecttd_list[i+1].project_percentage - projecttd_list[i].project_percentage
            ''' divisible by zero catch '''
            if _x == 0.0:
                _dydx = 0.0
            else:
                _dydx = _y/_x
            projecttd_list[i].derivative_value_temp = _dydx
        # set the last value
        projecttd_list[-1].derivative_value_temp = projecttd_list[-2].derivative_value

        print('updating database with derivative data for star repo: ' + _projectkey)
        ''' Update the data in the database. '''
        for td in projecttd_list:
            dbe.update_td(td_id=td.id, td=td)


def normalize_derivatives_menu():
    dbe.open()
    _projects = config.get_projects()
    _timeline = np.arange(0.00, 1.00, 0.01)
    for project in _projects:
        _projectkey = project['key']
        _repokey = project['github']
        print('Normalizing Project and Github: ' + _projectkey + ' : ' + _repokey)
        for i, val in enumerate(_timeline[:-1]):
            _derivative = dbe.get_derivative_data_between_percentage(_timeline[i],
                                                                     _timeline[i + 1],
                                                                     _repokey,
                                                                     _projectkey)
            dbe.insert_derivative(derivative_data=_derivative)
        ''' Insert the last one in the database '''
        _derivative.project_percentage = 1.0
        dbe.insert_derivative(derivative_data=_derivative)


def set_success_value_of_td_menu():
    dbe.open()
    _projects = config.get_projects()
    for project in _projects:
        print('updating the success value for project: ' + project['key'])
        _key = project['key']
        _td = dbe.import_tddata(projectkey=_key)
        _dydx = dbe.get_derivatives_by_project(projectkey=_key)

        ''' last value and current value of project percentage in order to get the things between those two values.'''
        _last = 0
        for dy in _dydx:
            _current = dy.project_percentage
            print('updating for project percentage: ' + str(_current))
            _newtd = list((t for t in _td if _last < t.project_percentage < _current))
            ''' update the successful value in the tds with the new successful value from derivative data. '''
            for _td_2_update in _newtd:
                _td_2_update.successful_temp = dy.successful
                dbe.update_td(td_id=_td_2_update.id, td=_td_2_update)
            _last = _current


def export_data_to_db(project=None, issuetypes=['Bug']):
    dbe.open()
    _project_events = __get_project_events(project=project, issuetypes=issuetypes)
    _project_events.sort()

    #cumlative sum
    total = 0
    for event in _project_events.events:
        total += event.event_value
        event.cumlative_value = total

    dbe.export_tddata(eventlist=_project_events.events, projectkey=project['key'], successful=project['success'])


def gettechnicaldebtbyproject(project=None, num_of_bins=None, issuetypes='Bug', by='percentage'):
    if project is not None:
        _project_events = __get_project_events(project=project, issuetypes=issuetypes)
        _values = None
        if num_of_bins is not None:
            _values = _project_events.get_cumlative_totals_by_bins(number_of_bins=num_of_bins)
        else:
            _values = _project_events.cumlative_event_totals(by=by)
        return _values
    else:
        return None


def __get_project_events(project=None, issuetypes='Bug'):
    jira = JIRAWrapper(jira_url=config.get_jira_url(),
                       jira_username=config.get_jira_username(),
                       jira_password=config.get_jira_password())
    if project is not None:
        _project_start_date = project['start_date']
        _project_end_date = project['end_date']
        _issues = jira.get_data(project_key=project['key'],
                                issues_type_str=issuetypes,
                                from_date_str=_project_start_date,
                                to_date_str=_project_end_date)
        _project_events = ProjectEventList(_issues, start_date=_project_start_date, end_date=_project_end_date)
        return _project_events
    else:
        return None


def plot_by_project_bins(project=None, num_of_bins=None, issuetypes='Bug', by='percentage'):
    _values = gettechnicaldebtbyproject(project=project, num_of_bins=num_of_bins, issuetypes=issuetypes, by=by)
    if _values is not None:
        _y = list(_values.values())
        _x = list(_values.keys())
        #plt.plot(_x, _y, '-ok')
        #plt.show()
        trace = go.Scatter(
            x=_x,
            y=_y,
            mode='lines'
        )

        data = [trace]

        # Plot and embed in ipython notebook!
        py.offline.plot({
            "data": data,
            "layout": go.Layout(title="Technical Debt")
        }, auto_open=True)
    else:
        print('error: _values is empty')


def menu():
    while 1:
        # Create the menu
        print("Technical Debt Calculator and Prediction")
        print("by Tommy Shrove")
        print("1. Technical Plot by Project")
        print("2. Export Data to Database")
        print("3. Projects' Basic Stats")
        print("4. Get GitHub Stats")
        print("5. Import Github Star Data")
        print("6. Normalize Star Data")
        print("7. Derivative of Star Data")
        print("8. Derivative of TD Data")
        print("9. Normalize Derivatives of TD and Star Data")
        print("A. Set Successful Value of Rechnical Debt Value Based on Derivative Data")
        print("")
        print("0. Exit")
        _menu_selection = input("Please choose a menu item: ")
        if _menu_selection == '1':
            technicaldebtbyproject_menu()
        elif _menu_selection == '2':
            exportdebttodatabase_menu()
        elif _menu_selection == '3':
            projectstats_menu()
        elif _menu_selection == '4':
            github_stats_menu()
        elif _menu_selection == '5':
            github_export_menu()
        elif _menu_selection == '6':
            github_normalize_menu()
        elif _menu_selection == '7':
            derivative_of_stardata_menu()
        elif _menu_selection == '8':
            derivative_of_tddata_menu()
        elif _menu_selection == '9':
            normalize_derivatives_menu()
        elif _menu_selection == 'A':
            set_success_value_of_td_menu()
        elif _menu_selection == '0':
            exit(0)
        else:
            pass


if __name__ == "__main__":
    main()
