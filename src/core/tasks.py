from celery import group
from celery import chain
from celery import subtask
from celery import Task


def map_single_task(args_list, *signatures):
    return group([
        subtask(signatures[0]).clone((args,))
        for args in args_list
    ])


def map_signature_chain(args_list, *signatures):
    return group([
        chain(
            subtask(signatures[0]).clone((args,)),
            *(subtask(sig) for sig in signatures[1:])
        ) for args in args_list
    ])


workflow_resolvers = {1: map_single_task}


class DistributeChain(Task):
    name = 'distribute_chain'
    ignore_results = True

    def run(self, result, *signatures, key):
        workflow_resolver = workflow_resolvers.get(
            len(signatures), map_signature_chain)

        args_list = result[key]
        group_task = workflow_resolver(args_list, *signatures)

        return group_task()
