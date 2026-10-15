#!/usr/bin/env python3

from _lib import (

    DATA_FILE,

    REGISTRY_FILE,

    load_json
)


def main():

    try:

        data = load_json(
            DATA_FILE
        )

        registry = load_json(
            REGISTRY_FILE
        )

        total_tasks = len(
            data["tasks"]
        )

        total_active = 0

        total_completed = 0

        total_steps = 0

        completed_steps = 0

        for task in data["tasks"]:

            if task[
                "status"
            ] == "active":

                total_active += 1

            elif task[
                "status"
            ] == "completed":

                total_completed += 1

            total_steps += len(
                task["steps"]
            )

            completed_steps += sum(

                1

                for step
                in task["steps"]

                if step["completed"]
            )

        print()

        print(
            "Database Validation Successful"
        )

        print()

        print(
            f"Total Tasks      : {total_tasks}"
        )

        print(
            f"Active Tasks     : {total_active}"
        )

        print(
            f"Completed Tasks  : {total_completed}"
        )

        print(
            f"Total Steps      : {total_steps}"
        )

        print(
            f"Completed Steps  : {completed_steps}"
        )

        print(
            f"Last Registry ID : "
            f"{registry['last_registry']}"
        )

        print(
            f"Last Task ID     : "
            f"{registry['last_task']}"
        )

        print()

    except Exception as e:

        print()

        print(
            "Validation Failed"
        )

        print()

        print(
            str(e)
        )

        print()


if __name__ == "__main__":

    main()
  
