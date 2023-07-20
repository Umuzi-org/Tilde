import dramatiq
import django
import sys


def actor(**dramatiq_actor_kwargs):
    def inner(actor_function):
        def final_actor_function(*args, **kwargs):
            try:
                print(
                    f"\n\nRunning {actor_function.__name__} with args {args} and kwargs {kwargs}"
                )
                result = actor_function(*args, **kwargs)
                print("...Finished running {actor_function.__name__}")
                return result
            except django.db.utils.InterfaceError:
                print("Exiting due to database error")
                # this will cause the entire worker process to die. The pod will restart and hopefully the problem will be resolved
                with open("/tmp/kill", "w") as f:
                    f.write("1")
                sys.exit(1)

        final_actor_function.__name__ = actor_function.__name__

        return dramatiq.actor(**dramatiq_actor_kwargs)(final_actor_function)

    return inner
