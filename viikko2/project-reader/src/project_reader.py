from urllib import request
from project import Project
import toml

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        content = request.urlopen(self._url).read().decode("utf-8")
        project_data = toml.loads(content)
        
        # Parse general information and add license and authors
        name = project_data['tool']['poetry']['name']
        description = project_data['tool']['poetry']['description']
        license = project_data['tool']['poetry'].get('license', '-')
        authors = project_data['tool']['poetry'].get('authors', [])

        dependencies = project_data['tool']['poetry']['dependencies']
        dev_dependencies = project_data['tool']['poetry']['group']['dev']['dependencies']

        return Project(name, description, license, authors, dependencies, dev_dependencies)


