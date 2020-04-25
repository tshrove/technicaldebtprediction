from github import Github


class GitHubWrapper:

    ###
    # Private Variable
    ###
    __repo_name = ""

    ###
    # Public Methods
    ###
    def __init__(self, username, password, repo):
        """ Default Constructor """
        self.__labels = ""
        self.gh = Github(login_or_token=username, password=password)
        self.__repo_name = repo

    def get_releases(self):
        _ghrepo = self.gh.get_repo(full_name_or_id=self.__repo_name)
        """ Still need to filter by the to_date range"""
        _contents = _ghrepo.get_clones_traffic()
        return _contents

    def get_stargazers(self):
        _ghrepo = self.gh.get_repo(full_name_or_id=self.__repo_name)
        _stars = _ghrepo.get_stargazers_with_dates()
        return _stars
