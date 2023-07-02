import pandas as pd
from collections import defaultdict
import os
import re

def invert_dictionary(mappings: dict):

    inverted_dict = defaultdict(list)

    for key, value in mappings.items():
        inverted_dict[value].append(key)

    return inverted_dict


class Repertoire:

    def __init__(self, name):
        self.name = name
        self.__filename = ""
        self.cdr3aa = {}

    @property
    def repertoire(self):

        return self._repertoire
    
    @repertoire.setter
    def repertoire(self, input) -> None:

        if isinstance(input, pd.DataFrame):
            self._repertoire = input

        elif isinstance(input, str):
            assert os.path.exists(input), f"No such file or directory: '{input}'"

            self.__filename = input
            self._repertoire = pd.read_csv(input, sep="\t")

        return None
    
    def parser(self) -> None:

        if not hasattr(self, "repertoire"):
            raise ValueError("problem message placeholder")

        vseg_def_unique = (
            self._repertoire[["CDR3aa", "V"]]
            .drop_duplicates() 
            .set_index("CDR3aa")["V"] 
            .apply(lambda v_seg_name: v_seg_name[:3])
            .to_dict()
        )

        self.cdr3aa = invert_dictionary(vseg_def_unique)

        return None

    def lookup(self, queryBySeq) -> pd.DataFrame:

        if not hasattr(self, "repertoire"):
            raise ValueError("problem message placeholder")
        
        return self._repertoire[self._repertoire["CDR3aa"] == queryBySeq]
    
    
class RepertoireCollection:

    collections = set()

    def __init__(self, collection):

        self.name = collection
        self.collections.add(collection)
        
        self.collection_members = {}

    @classmethod 
    def get_collections(cls):
        return cls.collections

    def add_from_folder(self, folder, i = 1) -> None:

        for file in os.listdir(folder):
                
            filepath = os.path.join(folder, file)

            if os.path.getsize(filepath) > 0:

                try:
                    name = re.search("ERR+[^_]+", filepath).group(0)
                except AttributeError:
                    name = f"unresolved name instance {i}"
                    i += 1
                
                _repertoire_instance = Repertoire(name)
                _repertoire_instance.repertoire = filepath
                _repertoire_instance.parser()

                self.collection_members[name] = _repertoire_instance

            else:

                pass

        return None

    def add_member(self, sample: object) -> None:

        self.collection_members[sample.name] = sample

        return None


    def del_member(self, samples: list) -> None:
        
        for i in samples:
            del self.collection_members[i]
            
        return None
