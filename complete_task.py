#!/usr/bin/env python3

import sys

from _lib import (

    DATA_FILE,

    load_json,

    save_json,

    find_task,

    calculate_progress,

    get_time_info,

    build_completion_report
)


def main():

    if len(sys.argv) != 2:

        print()

        print(
            "Usage:"
        )

        print()

        print(
            "python3 complete_task.py TASK-000001"
        )

        print()

        return

    task_id = sys.argv[1]

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
            f"Task not found: {task_id}"
        )

        print()

        return

    calculate_progress(
        task
    )

    total_steps = len(
        task["steps"]
    )

    completed_steps = task[
        "progress"
    ][
        "completed"
    ]

    if total_steps > 0:

        if completed_steps != total_steps:

            print()

            print(
                "Task cannot be completed."
            )

            print()

            print(
                f"Completed Steps : {completed_steps}"
            )

            print(
                f"Remaining Steps : "
                f"{task['progress']['remaining']}"
            )

            print()

            return

    if task["status"] == "completed":

        print()

        print(
            "Task already completed."
        )

        print()

        return

    time_info = get_time_info()

    overview, evaluation = (

        build_completion_report(
            task
        )
    )

    task[
        "status"
    ] = "completed"

    task[
        "completed_dhaka"
    ] = time_info["dhaka"]

    task[
        "completed_utc"
    ] = time_info["utc"]

    task[
        "overview"
    ] = overview

    task[
        "evaluation"
    ] = evaluation

    save_json(
        DATA_FILE,
        data
    )

    print()

    print(
        "=" * 60
    )

    print(
        "TASK COMPLETED"
    )

    print(
        "=" * 60
    )

    print()

    print(
        f"Task ID : {task_id}"
    )

    print(
        f"Registry: {task['registry']}"
    )

    print()

    print(
        overview
    )

    print()

    print(
        "Evaluation"
    )

    print(
        "-" * 60
    )

    print(
        f"Steps Total      : "
        f"{evaluation['steps_total']}"
    )

    print(
        f"Steps Completed  : "
        f"{evaluation['steps_completed']}"
    )

    print(
        f"Completion Rate  : "
        f"{evaluation['completion_percentage']}%"
    )

    print(
        f"Notes            : "
        f"{evaluation['notes']}"
    )

    print(
        f"Attachments      : "
        f"{evaluation['attachments']}"
    )

    print(
        f"Archive Ready    : "
        f"{evaluation['archive_ready']}"
    )

    print()


if __name__ == "__main__":

    main()
      
