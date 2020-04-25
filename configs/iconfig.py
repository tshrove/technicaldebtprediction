

class IConfig:
    """
    Interface object.
    """
    def __init__(self):
        pass

    def get_priority_values(self):
        pass

    def get_jira_url(self):
        pass

    def get_jira_username(self):
        pass

    def get_jira_password(self):
        pass

    def get_resolved_statuses(self):
        pass

    def get_projects(self):
        pass

    def get_issuetypes(self):
        pass

    def get_issuetrackertype(self):
        pass
