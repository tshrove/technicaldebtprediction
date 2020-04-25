

class IWrapper:
    """
    Interface object.
    """
    def __init__(self):
        pass

    def get_data(self, project_key, issue_type_str=None, from_date_str=None, to_date_str=None):
        pass

    def get_data_by_query(self, query_str):
        pass