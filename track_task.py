#!/usr/bin/env python3

import sys

from _lib import (

    DATA_FILE,

    load_json,

    save_json,

    get_time_info,

    find_task,

    calculate_progress
)


def ensure_history(task):

    if "history" not in task:

        task["history"] = []


def log_history(
    task,
    action,
    dhaka,
    utc
):

    ensure_history(task)

    task["history"].append({

        "dhaka":
        dhaka,

        "utc":
        utc,

        "action":
        action
    })


def print_task_status(task):

    progress = task["progress"]

    print()

    print(
        "=" * 60
    )

    print(
        "TASK STATUS"
    )

    print(
        "=" * 60
    )

    print()

    print(
        f"Task ID      : "
        f"{task['task_id']}"
    )

    print(
        f"Registry     : "
        f"{task['registry']}"
    )

    print(
        f"Status       : "
        f"{task['status']}"
    )

    print()

    print(
        f"Completed    : "
        f"{progress['completed']}"
    )

    print(
        f"Remaining    : "
        f"{progress['remaining']}"
    )

    print(
        f"Progress     : "
        f"{progress['percentage']}%"
    )

    print()


def main():

    if len(sys.argv) != 3:

        print()

        print(
            "Usage:"
        )

        print()

        print(
            "python3 track_task.py TASK-000001 1"
        )

        print()

        sys.exit(1)

    task_id = sys.argv[1]

    try:

        step_id = int(
            sys.argv[2]
        )

    except ValueError:

        print()

        print(
            "Step ID must be numeric."
        )

        print()

        sys.exit(1)

    data = load_json(
        DATA_FILE
    )

    task = find_task(
        task_id,
        data
    )

    if not task:

        print()

        print(
            f"Task not found: "
            f"{task_id}"
        )

        print()

        sys.exit(1)

    if task["status"] == "completed":

        print()

        print(
            "Task already completed."
        )

        print()

        sys.exit(1)

    target_step = None

    for step in task["steps"]:

        if step["id"] == step_id:

            target_step = step

            break

    if not target_step:

        print()

        print(
            f"Step not found: "
            f"{step_id}"
        )

        print()

        sys.exit(1)

    if target_step["completed"]:

        print()

        print(
            "Step already completed."
        )

        print()

        print(
            f"Step {step_id}: "
            f"{target_step['title']}"
        )

        print()

        sys.exit(0)

    time_info = get_time_info()

    target_step[
        "completed"
    ] = True

    target_step[
        "completed_dhaka"
    ] = time_info["dhaka"]

    target_step[
        "completed_utc"
    ] = time_info["utc"]

    calculate_progress(
        task
    )

    log_history(

        task,

        f"Completed Step "
        f"{step_id}: "
        f"{target_step['title']}",

        time_info["dhaka"],

        time_info["utc"]
    )

    save_json(
        DATA_FILE,
        data
    )

    print()

    print(
        "=" * 60
    )

    print(
        "STEP COMPLETED"
    )

    print(
        "=" * 60
    )

    print()

    print(
        f"Task ID : "
        f"{task_id}"
    )

    print()

    print(
        f"Step ID : "
        f"{step_id}"
    )

    print()

    print(
        f"Title   : "
        f"{target_step['title']}"
    )

    print()

    print(
        f"Dhaka   : "
        f"{time_info['dhaka']}"
    )

    print()

    print(
        f"UTC     : "
        f"{time_info['utc']}"
    )

    print()

    print_task_status(
        task
    )


if __name__ == "__main__":

    main()
      
