from pony.orm import *
from datetime import datetime
from .derivative import DerivativeData

db = Database()


class DBProjectTDEvent(db.Entity):
    id = PrimaryKey(int, auto=True)
    event_date = Required(datetime)
    project_percentage = Required(float)
    value = Required(float)
    cumlative_value = Required(float)
    projectkey = Required(str)


class DBProjectTDEvent4(db.Entity):
    id = PrimaryKey(int, auto=True)
    event_date = Required(datetime)
    project_percentage = Required(float)
    value = Required(float)
    cumlative_value = Required(float)
    projectkey = Required(str)
    successful = Optional(int, size=8)
    derivative_value = Optional(float)


class DBStar(db.Entity):
    id = PrimaryKey(int, auto=True)
    event_date = Required(datetime)
    repokey = Required(str)
    value = Required(int)
    cumlative_value = Required(int)
    normalized_percentage = Optional(float)
    derivative_value = Optional(float)


class DBDerivative(db.Entity):
    id = PrimaryKey(int, auto=True)
    project_percentage = Required(float)
    repokey = Required(str)
    projectkey = Required(str)
    star_derivative = Optional(float)
    td_derivative = Optional(float)
    successful = Required(int, size=8)


class MySQLExport:

    def __init__(self, host, username, password, database):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__isopen = False

    def open(self):
        if self.__isopen is False:
            db.bind(provider='mysql',
                    host=self.__host,
                    user=self.__username,
                    passwd=self.__password,
                    db=self.__database)
            db.generate_mapping(create_tables=True)
            self.__isopen = True

    @db_session
    def import_tddata(self, projectkey=None):
        _query = None
        if projectkey is None:
            _query = select(td for td in DBProjectTDEvent4)
        else:
            _query = select(td for td in DBProjectTDEvent4 if td.projectkey == projectkey)
        return list(_query)

    @db_session
    def export_tddata(self, eventlist=None, projectkey="<None>", successful=-1):
        if eventlist is None:
            return False

        if self.__isopen is False:
            return False

        for event in eventlist:
            db_event = DBProjectTDEvent4(event_date=event.event_date,
                                         project_percentage=event.project_percentage,
                                         value=event.event_value,
                                         cumlative_value=event.cumlative_value,
                                         projectkey=projectkey,
                                         successful=successful)

        return True

    @db_session
    def export_stardata(self, star_list=None, repokey="<None>"):
        if star_list is None:
            return False

        if repokey is "<None>":
            return False

        if self.__isopen is False:
            return False

        _count = self.get_starcount(repokey=repokey)

        # This is to get the count starting at 1 instead of zero
        if _count is 0:
            _count = _count + 1

        for star in star_list:
            DBStar(event_date=star.starred_at, repokey=repokey, value=1, cumlative_value=_count)
            _count = _count + 1

        return True

    @db_session
    def import_stardata(self, repo_name=None):
        _query = None
        if repo_name is None:
            _query = select(star for star in DBStar)
        else:
            _query = select(star for star in DBStar if star.repokey == repo_name)
        return list(_query)

    @db_session
    def import_derivativedata(self, repo_name=None, projectkey=None):
        _querystar = list(select(star for star in DBStar if star.repokey == repo_name))
        _querytd = list(select(td for td in DBProjectTDEvent4 if td.projectkey == projectkey))
        return {'projectkey': projectkey, 'repokey': repo_name, 'star_dydx': _querystar, 'td_dydx': _querytd}

    @db_session
    def get_derivative_data_between_percentage(self, ratio_start, ratio_end, repokey, projectkey):
        ''' Get data '''
        _star_derivative = list(select(star for star in DBStar if star.repokey == repokey))
        _td_derivative = list(select(td for td in DBProjectTDEvent4 if td.projectkey == projectkey))

        ''' Filter it down '''
        _star_derivative = [star.derivative_value for star in _star_derivative if ratio_start < star.normalized_percentage <= ratio_end]
        _td_derivative = [td.derivative_value for td in _td_derivative if ratio_start < td.project_percentage <= ratio_end]

        return DerivativeData(project_percentage=ratio_end,
                              repokey=repokey,
                              projectkey=projectkey,
                              star_derivative_list=_star_derivative,
                              td_derivative_list=_td_derivative)

    @db_session
    def get_derivatives_by_project(self, projectkey):
        _project_derivatives = list(select(d for d in DBDerivative if d.projectkey == projectkey))
        return _project_derivatives

    @db_session
    def get_star(self, id):
        return DBStar.get(id=id)

    @db_session
    def update_star(self, star_id, star):
        _s = DBStar.get(id=star_id)
        _s.event_date = star.event_date
        _s.repokey = star.repokey
        _s.value = star.value
        _s.cumlative_value = star.cumlative_value
        if hasattr(star, 'normalized_percentage_temp'):
            _s.normalized_percentage = star.normalized_percentage_temp
        if hasattr(star, 'derivative_value_temp'):
            _s.derivative_value = star.derivative_value_temp

    @db_session
    def update_td(self, td_id, td):
        _s = DBProjectTDEvent4.get(id=td_id)
        _s.event_date = td.event_date
        _s.project_percentage = td.project_percentage
        _s.value = _s.value
        _s.cumlative_value = td.cumlative_value
        _s.projectkey = td.projectkey
        if hasattr(td, 'successful_temp'):
            _s.successful = td.successful_temp
        if hasattr(td, 'derivative_value_temp'):
            _s.derivative_value = td.derivative_value_temp

    @db_session
    def insert_derivative(self, derivative_data):
        if type(derivative_data) is not DerivativeData:
            return None

        DBDerivative(project_percentage=derivative_data.project_percentage,
                     repokey=derivative_data.repokey,
                     projectkey=derivative_data.projectkey,
                     star_derivative=derivative_data.get_mean_of_star_data(),
                     td_derivative=derivative_data.get_mean_of_td_data(),
                     successful=derivative_data.is_successful())

    @db_session
    def get_starcount(self, repokey):
        return count(s for s in DBStar if s.repokey is repokey)

    @db_session
    def deletedata(self):
        # delete everything in table first.
        delete(e for e in DBProjectTDEvent4)

    @db_session
    def deletestardata(self):
        delete(e for e in DBStar)
