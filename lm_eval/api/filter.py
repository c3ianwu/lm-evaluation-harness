from typing import List

from lm_eval.api.instance import Instance

class Filter:
    """
    Filter classes operate on a per-task level. 
    They take all model outputs (`instance.resps` for all `task.instances`)
    across all instances of a task, and perform operations.
    In a single run, one can configure any number of separate filters or lists of filters.

    """

    def __init__(self):
        """
        Can define custom behavior here, if an individual instantiation of a Filter class should have state.
        """

    def apply(self, resps):
        """
        Defines the operation to perform on a list of the `inst.resps` properties of `Instance` objects.
        Should return the list of (filtered) response lists *in the same order as they were input*, e.g.
        if pass in [<inst.resps for instance 0>, <inst.resps for instance 1>] should return
        [<filtered resps for instance 0>, <filtered resps for instance 1>]
        """
        return resps
        

class FilterEnsemble():
    """
    FilterEnsemble creates a pipeline applying multiple filters.
    Its intended usage is to stack multiple post-processing steps in order. 
    `task.apply_filters` should use a list of FilterEnsemble classes that it stores, to apply each 
    pipeline separately.
    """

    def __init__(self, name: str = None, components=List[Filter]):
        """
        Initializes a FilterEnsemble with name `name` and `components` as its filters, in order. 
        """
        # name defines the key that will be used to identity the filtered_resps produced by this pipeline.
        self.name = name

        self.filters = components

    def apply(self, instances: List[Instance]):

        resps = [inst.resps for inst in instances] # operate just on the model responses
        for f in self.filters:
            # apply filters in sequence
            out = f.apply(resps)
            resps = out # TODO: handle the case where a filter returns multiple "buckets"
        
        # add the end results after filtering to filtered_requests of their respective source instances.
        # 
        for inst, resp in zip(instances, resps):
            inst.filtered_resps[self.name] = resp

            
