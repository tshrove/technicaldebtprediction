import numpy as np


class DerivativeData:
    ###
    # Public Methods
    ###
    def __init__(self, project_percentage, repokey, projectkey, star_derivative_list, td_derivative_list):
        """ Default Constructor """
        self.project_percentage = project_percentage
        self.repokey = repokey
        self.projectkey = projectkey
        self.star_derivative_list = star_derivative_list
        self.td_derivative_list = td_derivative_list

    def get_mean_of_star_data(self):
        if len(self.star_derivative_list) > 0:
            _val = np.mean(self.star_derivative_list)
            return _val
        else:
            return 0

    def get_mean_of_td_data(self):
        if len(self.td_derivative_list) > 0:
            _val = np.mean(self.td_derivative_list)
            return _val
        else:
            return 0

    def __is_failure_star(self):
        if self.get_mean_of_star_data() < 5000:
            return True
        else:
            return False

    def __is_failure_td(self):
        if self.get_mean_of_td_data() > 0:
            return True
        else:
            return False

    def is_successful(self):
        if self.__is_failure_star() is True and self.__is_failure_td() is True:
            return False
        else:
            return True

