from automarker_app.lib.marker import get_steps_final_status, get_final_review


def print_steps_result(steps):
    print()
    for step in steps:
        print(f"STEP: {step.name} ")
        print(f"\tDuration: {step.duration()}")
        print(f"\tStatus: {step.status}")
        if step.message:
            print(f"\tMessage: {step.message}")
        if step.details:
            print(f"\tDetails:")
            print(step.details_string())
        print()

    print(f"FINAL STATUS: {get_steps_final_status(steps)}")


def print_final_review(steps):
    final_status, comments = get_final_review(steps)
    print("----------------------------------------")
    print("# REVIEW:\n")
    print(f"FINAL REVIEW STATUS: {final_status}\n")
    print(comments)
    print("----------------------------------------")
