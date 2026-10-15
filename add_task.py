#!/usr/bin/env python3

import argparse

from _lib import (
    ensure_structure,
    load_json,
    save_json,
    DATA_FILE,
    generate_ids,
    get_time_info,
    create_steps,
    store_attachment
)


def main():

    ensure_structure()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "heading"
    )

    parser.add_argument(
        "description"
    )

    parser.add_argument(
        "--steps",
        default=""
    )

    parser.add_argument(
        "--add-note",
        action="append",
        default=[]
    )

    parser.add_argument(
        "--add-file",
        action="append",
        default=[]
    )

    args = parser.parse_args()

    task_id, reg_id = generate_ids()

    time_info = get_time_info()

    attachments = []

    for file_path in args.add_file:

        attachment = store_attachment(
            task_id,
            file_path
        )

        if attachment:

            attachments.append(
                attachment
            )

    steps = create_steps(
        args.steps
    )

    task = {

        "task_id":
        task_id,

        "registry":
        reg_id,

        "status":
        "active",

        "heading":
        args.heading,

        "description":
        args.description,

        "created_dhaka":
        time_info["dhaka"],

        "created_utc":
        time_info["utc"],

        "notes":
        args.add_note,

        "attachments":
        attachments,

        "steps":
        steps,

        "progress": {

            "completed": 0,

            "remaining":
            len(steps),

            "percentage": 0
        }
    }

    data = load_json(
        DATA_FILE
    )

    data["tasks"].insert(
        0,
        task
    )

    save_json(
        DATA_FILE,
        data
    )

    print()
    print(
        "Task Added Successfully"
    )

    print()

    print(
        f"Task ID  : {task_id}"
    )

    print(
        f"Registry : {reg_id}"
    )

    print(
        f"Heading  : {args.heading}"
    )

    print(
        f"Steps    : {len(steps)}"
    )

    print(
        f"Files    : {len(attachments)}"
    )

    print()


if __name__ == "__main__":
    main()
  
