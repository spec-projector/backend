from cloudant.client import CouchDB
from cloudant.document import Document
import json

USERNAME = 'admin'
PASSWORD = 'admin'
URL = 'http://127.0.0.1:5984'
client = CouchDB(USERNAME, PASSWORD, url=URL, connect=True, auto_renew=True)
db = client['b6a0cce0-fa1b-45e8-bbb2-3ff859ad8a0c']


class General:
    def __init__(self, db: CouchDB, id: str):
        self._db = db
        with Document(db, id) as doc:
            self._doc = doc
        self._title = None
        self._name = None
        self._graphql = None
        self._fields = None
        self._entities = None
        self._api = None
        self._workflow = None
        self._features = None
        self._version = None
        self._model = None
        self._tools = None
        self._resourceTypes = None
        self._actors = None
        self._modules = None
        self._terms = None

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = self._doc['name']
        return self._name

    @property
    def title(self) -> str:
        if self._title is None:
            self._title = self._doc['title']
        return self._title


class Graphql(General):
    def to_dict(self) -> dict:
        return {
            "title": self.title
        }


class Workflow(General):
    def to_dict(self) -> dict:
        return {
            "story": self._doc['story']
        }


class Api(General):
    @property
    def graphql(self) -> list:
        if self._graphql is None:
            self._graphql = self._load_graphql()
        return self._graphql

    def _load_graphql(self) -> list:
        return [Graphql(self._db, doc_graphql['_id']) for doc_graphql in self._doc['graphql']]

    def to_dict(self) -> dict:
        return {
            "_id": self._doc['_id'],
            "graphql": [graphql.to_dict() for graphql in self.graphql]
        }


class Tool(General):
    def to_dict(self) -> dict:
        return {
            "_id": self._doc['_id']
        }


class Field(General):
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "name": self.name
        }


class Entity(General):
    @property
    def fields(self) -> list:
        if self._fields is None:
            self._fields = self._load_fields()
        return self._fields

    def _load_fields(self) -> list:
        return [Field(self._db, doc_fields['_id']) for doc_fields in self._doc['fields']]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "entities": [entity.to_dict() for entity in self.fields]
        }


class Model(General):
    @property
    def entities(self) -> list:
        if self._entities is None:
            self._entities = self._load_entities()
        return self._entities

    def _load_entities(self) -> list:
        return [Entity(self._db, doc_entity['_id']) for doc_entity in self._doc['entities']]

    def to_dict(self) -> dict:
        return {
            "title": '-',
            "entities": [entity.to_dict() for entity in self.entities]
        }


class Feature(General):
    @property
    def title_text(self) -> str:
        if self._title is None:
            self._title = self._doc['title'][0]['text']
        return self._title

    @property
    def api(self) -> Api:
        if self._api is None:
            self._api = Api(self._db, self._doc['api']['_id'])
        return self._api

    def api_to_dict(self):
        try:
            return self.api.to_dict()
        except KeyError:
            return self._api

    @property
    def workflow(self) -> Workflow:
        if self._workflow is None:
            self._workflow = Workflow(self._db, self._doc['workflow']['_id'])
        return self._workflow

    def workflow_to_dict(self):
        try:
            return self.workflow.to_dict()
        except KeyError:
            return self._workflow

    def to_dict(self) -> dict:
        if self.api_to_dict() is None and self.workflow_to_dict() is None:
            return {
                "title": self.title_text,
            }
        elif self.api_to_dict() is None:
            return {
                "title": self.title_text,
                "workflow": self.workflow_to_dict()
            }
        elif self.workflow_to_dict() is None:
            return {
                "title": self.title_text,
                "api": self.api_to_dict()
            }
        else:
            return {
                "title": self.title_text,
                "api": self.api_to_dict(),
                "workflow": self.workflow_to_dict()
            }


class Term(General):
    def to_dict(self) -> dict:
        return {
            "name": self.name,
        }


class Module(General):
    @property
    def features(self) -> list:
        if self._features is None:
            self._features = self._load_features()
        return self._features

    def _load_features(self) -> list:
        return [Feature(self._db, doc_features['_id']) for doc_features in self._doc['features']]

    def to_dict(self) -> dict:
        return {
            "name": self.title,
            "features": [feature.to_dict() for feature in self.features]
        }


class Actor(General):
    @property
    def features(self) -> list:
        if self._features is None:
            self._features = self._load_features()
        return self._features

    def _load_features(self) -> list:
        return [Feature(self._db, doc_features['_id']) for doc_features in self._doc['features']]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "features": [feature.to_dict() for feature in self.features]
        }


class ProjectSpecification(General):
    @property
    def version(self) -> str:
        if self._version is None:
            self._version = self._doc['scheme']['version']
        return self._version

    @property
    def model(self) -> Model:
        if self._model is None:
            self._model = Model(self._db, self._doc['model']['_id'])
        return self._model

    @property
    def tools(self) -> Tool:
        if self._tools is None:
            self._tools = Tool(self._db, self._doc['model']['_id'])
        return self._tools

    @property
    def resourceTypes(self) -> list:
        if self._resourceTypes is None:
            self._resourceTypes = self._load_resourceTypes()
        return self._resourceTypes

    def _load_resourceTypes(self) -> list:
        return [rT['title'] for rT in self._doc['resourceTypes']]

    @property
    def actors(self) -> list:
        if self._actors is None:
            self._actors = self._load_actors()
        return self._actors

    def _load_actors(self) -> list:
        return [Actor(self._db, doc_actors['_id']) for doc_actors in self._doc['actors']]

    @property
    def modules(self) -> list:
        if self._modules is None:
            self._modules = self._load_modules()
        return self._modules

    def _load_modules(self) -> list:
        return [Module(self._db, doc_module['_id']) for doc_module in self._doc['modules']]

    @property
    def terms(self) -> list:
        if self._terms is None:
            self._terms = self._load_terms()
        return self._terms

    def _load_terms(self) -> list:
        return [Term(self._db, doc_term['_id']) for doc_term in self._doc['terms']]

    def to_dict(self) -> dict:
        return {
            'version': self.version,
            'model': self.model.to_dict(),
            'tools': self.tools.to_dict(),
            'resourceTypes': self.resourceTypes,
            'actors': [actor.to_dict() for actor in self.actors],
            'modules': [module.to_dict() for module in self.modules],
            'terms': [term.to_dict() for term in self.terms]
        }

    def _get_id_list_in_document(self, id2: str) -> list:
        s = []
        with Document(db, id2) as doc:
            for i1 in doc:
                y = doc[i1]
                if str(i1) == '_id':
                    s.append([str(y), ":"])
                if type(y) == list:
                    for i2 in y:
                        for i3 in i2:
                            if str(i3) == "_id":
                                s.append([str(i1), str(i2[i3])])
                elif type(y) == dict or type(y) == str:
                    for i2 in y:
                        if type(i2) != str or len(i2) != 1:
                            if str(i2) == '_id':
                                s.append([str(i1), str(y[i2])])
        return s

    def show_ids_in_database(self) -> print:
        s1 = self._get_id_list_in_document('spec')
        p = "    "
        for i1 in s1:
            print(p * 0 + i1[0])
            if i1[1] != ":":
                s2 = self._get_id_list_in_document(i1[1])
                for i2 in s2:
                    print(p * 1 + i2[0])
                    if i2[1] != ":":
                        s3 = self._get_id_list_in_document(i2[1])
                        for i3 in s3:
                            print(p * 2 + i3[0])
                            if i3[1] != ":":
                                s4 = self._get_id_list_in_document(i3[1])
                                for i4 in s4:
                                    print(p * 3 + i4[0])
                                    if i4[1] != ":":
                                        s5 = self._get_id_list_in_document(i4[1])
                                        for i5 in s5:
                                            print(p * 4 + i5[0])
                                            if i5[1] != ":":
                                                s6 = self._get_id_list_in_document(i5[1])
                                                for i6 in s6:
                                                    print(p * 5 + i6[0])
                                                    if i6[1] != ":":
                                                        print(p * 6 + i6[1])
# ProjectSpecification(db, 'spec').show_ids_in_database()


class SpecRepresenter():
    def __init__(self, spec: ProjectSpecification):
        self._spec = spec

    def print(self) -> print:
        dict = self._spec.to_dict()
        print(json.dumps(dict, indent=4, ensure_ascii=False))


def load_spec(db: CouchDB) -> print:
    spec = ProjectSpecification(db, 'spec')
    printer = SpecRepresenter(spec)
    printer.print()

load_spec(db)
