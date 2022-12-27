from utils.singleton import SingletonType

class Services(object, metaclass=SingletonType):
    azure = {}
    cosmo = {}
    organization = {}
    workspace = {}
    solution = {}
    connector = {}

    def __set__(self, azure, cosmo, organization, workspace, solution, connector, connector_type = ""):
        self.azure = azure
        self.cosmo = cosmo
        self.organization = organization
        self.workspace = workspace
        self.solution = solution
        self.connector = {
            'id': connector.get('id'),
            'type': connector_type,
            'name': connector.get('name'),
            'url': connector.get('url'),
        }
