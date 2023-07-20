import dramatiq
import django
import sys


def actor(**dramatiq_actor_kwargs):
    def inner(actor_function):
        def final_actor_function(*args, **kwargs):
            try:
                return actor_function(*args, **kwargs)
            except django.db.utils.InterfaceError:
                print("Exiting due to database error")
                # this will cause the entire worker process to die. The pod will restart and hopefully the problem will be resolved
                sys.exit(1)

        return dramatiq.actor(**dramatiq_actor_kwargs)(final_actor_function)

    return inner
