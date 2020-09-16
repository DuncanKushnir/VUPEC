"""
common functions used by most modules
"""
import json


class ObjDict(dict):
    """
    Allow using dicts as namespaces, eg {a:1, b:2} -> obj.a  (1)
    Also implements json interface
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError("No such attribute: {}".format(key))

    def __setattr__(self, key, val):
        if isinstance(val, dict):
            val = ObjDict.wrap_dict(val)

        self[key] = val

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError("No such attribute: {}".format(key))

    @staticmethod
    def wrap_dict(dictionary):
        """
        :param dictionary: a dict to wrap
        :return: an ObjDict, with sub_dictionaries recursively wrapped
        """
        new_dict = {
            k: ObjDict.wrap_dict(v) if isinstance(v, dict) else v
            for k, v in dictionary.items()
        }
        return ObjDict(new_dict)

    def to_json(self):
        return json.dumps(self, sort_keys=True)

    @staticmethod
    def from_json(json_string):
        return ObjDict.wrap_dict(json.loads(json_string))

    def is_resolved(self):
        """
        :return: a boolean indicating if the drive cycle contains references (False)
        or if all segments have been sourced and initialized correctly
        """
        if self._include:
            return False
        return True

    def resolve(self, data_structure):
        """
        given a datastructure that should contain the keys for any references,
        load and include the references to complete the drive cycle.
        """
        if not self.is_resolved():
            self.resolve_inclusions(data_structure)

    def resolve_inclusions(self, data_structure):
        """
        given a datastructure that should contain the keys for any references,
        load and include the references to complete the drive cycle.
        """
        overrides = {k: v for k, v in self.items()}
        self.clear()
        for item in overrides.get("_include", []):
            inclusion = data_structure.get(item, {})
            self.update(inclusion)

        if "_include" in overrides:
            del overrides["_include"]

        self.update(overrides)
