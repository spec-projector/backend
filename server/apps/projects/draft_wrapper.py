import json
from typing import Dict, List, Optional, Union

from cloudant.client import CouchDB
from cloudant.document import Document

USERNAME = "admin"
PASSWORD = "admin"
URL = "http://127.0.0.1:5984"
client = CouchDB(USERNAME, PASSWORD, url=URL, connect=True, auto_renew=True)
client_couchdb = client["b6a0cce0-fa1b-45e8-bbb2-3ff859ad8a0c"]


class General:
    """Base class for all classes from the CouchDB shell."""

    _title: str = None
    _name: str = None

    def __init__(self, db_couch: CouchDB, id_doc: str):
        """General variable."""
        self._db_couch = db_couch
        with Document(db_couch, id_doc) as doc:
            self._doc = doc

    @property
    def name(self) -> str:
        """Returns name of document."""
        if self._name is None:
            self._name = self._doc["name"]
        return self._name

    @property
    def title(self) -> str:
        """Returns title of document."""
        if self._title is None:
            self._title = self._doc["title"]
        return self._title


class Term(General):
    """Term class. Terms is listed in the "spec" document."""

    def to_dict(self) -> Dict[str, str]:
        """Returns dictionary with name of document."""
        return {"name": self.name}


class Workflow(General):
    """Workflow class. Workflow are listed in documents of type "features"."""

    def to_dict(self) -> Dict[str, str]:
        """Returns dictionary with name of document workflow history."""
        return {"story": self._doc["story"]}


class Graphql(General):
    """Graphql class. Graphql are listed in documents of type "api"."""

    def to_dict(self) -> Dict[str, str]:
        """Returns dictionary with title of document."""
        return {"title": self.title}


class Api(General):
    """Api class. Api are listed in documents of type "features"."""

    _graphql: List[Graphql] = None

    @property
    def graphql(self) -> Optional[List[Graphql]]:
        """Returns list of Graphql objects."""
        if self._graphql is None:
            self._graphql = self._load_graphql()
        return self._graphql

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "_id": self._doc["_id"],
            "graphql": [graphql.to_dict() for graphql in self.graphql],
        }

    def _load_graphql(self) -> List[Graphql]:
        return [
            Graphql(self._db_couch, doc_graphql["_id"])
            for doc_graphql in self._doc["graphql"]
        ]


class Feature(General):
    """
    Feature class.

    Features are listed in documents of type "Module" and "Actor".
    """

    _api: Api = None
    _workflow: Workflow = None

    @property
    def title_text(self) -> Optional[str]:
        """Returns title of document."""
        if self._title is None:
            self._title = self._doc["title"][0]["text"]
        return self._title

    @property
    def api(self) -> Optional[Api]:
        """Returns Api object."""
        if self._api is None:
            self._api = Api(self._db_couch, self._doc["api"]["_id"])
        return self._api

    @property
    def workflow(self) -> Optional[Workflow]:
        """Returns Workflow object."""
        if self._workflow is None:
            self._workflow = Workflow(
                self._db_couch,
                self._doc["workflow"]["_id"],
            )
        return self._workflow

    def api_to_dict(self) -> Union[Dict[str, str], None]:
        """Returns dictionary."""
        try:
            return self.api.to_dict()
        except KeyError:
            return None

    def workflow_to_dict(self) -> Union[Dict[str, str], None]:
        """Returns dictionary."""
        try:
            return self.workflow.to_dict()
        except KeyError:
            return None

    def to_dict(self) -> Dict[str, Union[str, List[str]]]:
        """Returns dictionary."""
        if self.api_to_dict() is None and self.workflow_to_dict() is None:
            return {
                "title": self.title_text,
            }
        elif self.api_to_dict() is None:
            return {
                "title": self.title_text,
                "workflow": self.workflow_to_dict(),
            }
        elif self.workflow_to_dict() is None:
            return {"title": self.title_text, "api": self.api_to_dict()}
        return {
            "title": self.title_text,
            "api": self.api_to_dict(),
            "workflow": self.workflow_to_dict(),
        }


class Actor(General):
    """Actor class. Actors are listed in the "spec" document."""

    _features: List[Feature] = None

    @property
    def features(self) -> Optional[List[Feature]]:
        """Returns list of Feature objects."""
        if self._features is None:
            self._features = self._load_features()
        return self._features

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "name": self.name,
            "features": [feature.to_dict() for feature in self.features],
        }

    def _load_features(self) -> List[Feature]:
        return [
            Feature(self._db_couch, doc_features["_id"])
            for doc_features in self._doc["features"]
        ]


class Module(General):
    """Module class. Modules are listed in the "spec" document."""

    _features: List[Feature] = None

    @property
    def features(self) -> Optional[List[Feature]]:
        """Returns list of Feature objects."""
        if self._features is None:
            self._features = self._load_features()
        return self._features

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "name": self.title,
            "features": [feature.to_dict() for feature in self.features],
        }

    def _load_features(self) -> List[Feature]:
        return [
            Feature(self._db_couch, doc_features["_id"])
            for doc_features in self._doc["features"]
        ]


class Tool(General):
    """Tool class. The tool is listed in the "spec" document."""

    def to_dict(self) -> Dict[str, str]:
        """Returns dictionary."""
        return {"_id": self._doc["_id"]}


class Field(General):
    """Field class. The fields are listed in documents of type "entities"."""

    def to_dict(self) -> Dict[str, str]:
        """Returns dictionary."""
        return {"title": self.title, "name": self.name}


class Entity(General):
    """Entity class. Entities are listed in documents of type "model"."""

    _fields: List[Field] = None

    @property
    def fields(self) -> Optional[List[Field]]:
        """Returns list of Field objects."""
        if self._fields is None:
            self._fields = self._load_fields()
        return self._fields

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "title": self.title,
            "fields": [field.to_dict() for field in self.fields],
        }

    def _load_fields(self) -> List[Field]:
        return [
            Field(self._db_couch, doc_fields["_id"])
            for doc_fields in self._doc["fields"]
        ]


class Model(General):
    """Model class. The model is listed in the "spec" document."""

    _entities: List[Entity] = None

    @property
    def entities(self) -> Optional[List[Entity]]:
        """Returns list of Entity objects."""
        if self._entities is None:
            self._entities = self._load_entities()
        return self._entities

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "title": "-",
            "entities": [entity.to_dict() for entity in self.entities],
        }

    def _load_entities(self) -> List[Entity]:
        return [
            Entity(self._db_couch, doc_entity["_id"])
            for doc_entity in self._doc["entities"]
        ]


class ProjectSpecification(General):
    """Stores and collects the project specification."""

    _version: str = None
    _model: Model = None
    _tools: Tool = None
    _resource_types: List[str] = None
    _actors: List[Actor] = None
    _modules: List[Module] = None
    _terms: List[Term] = None

    @property
    def version(self) -> Optional[str]:
        """Version function. The version is listed in the "spec" document."""
        if self._version is None:
            self._version = self._doc["scheme"]["version"]
        return self._version

    @property
    def model(self) -> Optional[Model]:
        """Returns Model object."""
        if self._model is None:
            self._model = Model(self._db_couch, self._doc["model"]["_id"])
        return self._model

    @property
    def tools(self) -> Optional[Tool]:
        """Returns Tool object."""
        if self._tools is None:
            self._tools = Tool(self._db_couch, self._doc["model"]["_id"])
        return self._tools

    @property
    def resource_types(self) -> Optional[List[str]]:
        """
        Resource types function.

        The resource types are listed in the "spec" document.
        """
        if self._resource_types is None:
            self._resource_types = self._load_resource_types()
        return self._resource_types

    @property
    def actors(self) -> Optional[List[Actor]]:
        """Returns list of ActorOrModule objects."""
        if self._actors is None:
            self._actors = self._load_actors()
        return self._actors

    @property
    def modules(self) -> Optional[List[Module]]:
        """Returns list of ActorOrModule objects."""
        if self._modules is None:
            self._modules = self._load_modules()
        return self._modules

    @property
    def terms(self) -> Optional[List[Term]]:
        """Returns list of Term objects."""
        if self._terms is None:
            self._terms = self._load_terms()
        return self._terms

    def to_dict(self) -> Dict[str, any]:
        """Returns dictionary."""
        return {
            "version": self.version,
            "model": self.model.to_dict(),
            "tools": self.tools.to_dict(),
            "resourceTypes": self.resource_types,
            "actors": [actor.to_dict() for actor in self.actors],
            "modules": [module.to_dict() for module in self.modules],
            "terms": [term.to_dict() for term in self.terms],
        }

    def _load_resource_types(self) -> List[str]:
        return [
            resource_type["title"]
            for resource_type in self._doc["resourceTypes"]
        ]

    def _load_actors(self) -> List[Actor]:
        return [
            Actor(self._db_couch, doc_actors["_id"])
            for doc_actors in self._doc["actors"]
        ]

    def _load_modules(self) -> List[Module]:
        return [
            Module(self._db_couch, doc_module["_id"])
            for doc_module in self._doc["modules"]
        ]

    def _load_terms(self) -> List[Term]:
        return [
            Term(self._db_couch, doc_term["_id"])
            for doc_term in self._doc["terms"]
        ]


def load_spec(db_couch: CouchDB) -> json:
    """Dumps database shell."""
    spec = ProjectSpecification(db_couch, "spec")
    spec_dict = spec.to_dict()
    return json.dumps(spec_dict, indent=4, ensure_ascii=False)


load_spec(client_couchdb)
