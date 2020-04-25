from .colsasoftwarefactoryconfig import ColsaSoftwareFactoryConfig
from .thesoftwarefactoryconfig import TheSoftwareFactoryConfig
from .mongodbconfig import MongoDBConfig
from .greenshotconfig import GreenshotConfig
from .hibernateconfig import HibernateConfig

configtype = "MONGODB"
#configtype = "HIBERNATE"
#configtype = "GREENSHOT"


class ConfigFactory:
    @staticmethod
    def factory():
        if configtype == "MONGODB":
            return MongoDBConfig()
        elif configtype == "HIBERNATE":
            return HibernateConfig()
        elif configtype == "GREENSHOT":
            return GreenshotConfig()
        else:
            return None
