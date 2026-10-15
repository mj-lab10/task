#!/usr/bin/env python3

import os
import json
import shutil
import hashlib
import mimetypes

from datetime import (
    datetime,
    timezone,
    timedelta
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data.json"
)

REGISTRY_FILE = os.path.join(
    BASE_DIR,
    "registry.json"
)

ATTACHMENTS_DIR = os.path.join(
    BASE_DIR,
    "attachments"
)


def ensure_structure():

    os.makedirs(
        ATTACHMENTS_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        DATA_FILE
    ):

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "tasks": []
                },
                f,
                indent=4,
                ensure_ascii=False
            )

    if not os.path.exists(
        REGISTRY_FILE
    ):

        with open(
            REGISTRY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "last_registry": 0,
                    "last_task": 0
                },
                f,
                indent=4,
                ensure_ascii=False
            )


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_time_info():

    utc_now = datetime.now(
        timezone.utc
    )

    dhaka_tz = timezone(
        timedelta(hours=6)
    )

    dhaka_now = utc_now.astimezone(
        dhaka_tz
    )

    return {

        "dhaka":
        dhaka_now.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3],

        "utc":
        utc_now.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
    }


def generate_ids():

    registry = load_json(
        REGISTRY_FILE
    )

    registry[
        "last_registry"
    ] += 1

    registry[
        "last_task"
    ] += 1

    task_id = (
        f"TASK-{registry['last_task']:06}"
    )

    reg_id = (
        f"REG-{registry['last_registry']:06}"
    )

    save_json(
        REGISTRY_FILE,
        registry
    )

    return (
        task_id,
        reg_id
    )


def sha256_file(path):

    digest = hashlib.sha256()

    with open(
        path,
        "rb"
    ) as f:

        while True:

            chunk = f.read(
                4096
            )

            if not chunk:
                break

            digest.update(
                chunk
            )

    return digest.hexdigest()


def store_attachment(
    task_id,
    file_path
):

    if not os.path.isfile(
        file_path
    ):
        return None

    filename = os.path.basename(
        file_path
    )

    extension = os.path.splitext(
        filename
    )[1]

    save_name = (
        task_id +
        extension
    )

    destination = os.path.join(
        ATTACHMENTS_DIR,
        save_name
    )

    shutil.copy2(
        file_path,
        destination
    )

    return {

        "file":
        f"attachments/{save_name}",

        "original":
        filename,

        "size":
        os.path.getsize(
            destination
        ),

        "mime":
        (
            mimetypes.guess_type(
                destination
            )[0]
            or
            "application/octet-stream"
        ),

        "sha256":
        sha256_file(
            destination
        )
    }


def create_steps(
    step_string
):

    steps = []

    if not step_string:

        return steps

    items = [

        item.strip()

        for item in step_string.split(",")

        if item.strip()
    ]

    counter = 1

    for item in items:

        steps.append({

            "id":
            counter,

            "title":
            item,

            "completed":
            False,

            "completed_dhaka":
            None,

            "completed_utc":
            None
        })

        counter += 1

    return steps


def calculate_progress(
    task
):

    total_steps = len(
        task["steps"]
    )

    if total_steps == 0:

        task["progress"] = {

            "completed": 0,

            "remaining": 0,

            "percentage": 0
        }

        return

    completed_steps = sum(

        1

        for step in task["steps"]

        if step["completed"]
    )

    remaining_steps = (
        total_steps -
        completed_steps
    )

    percentage = int(

        (
            completed_steps /
            total_steps
        ) * 100
    )

    task["progress"] = {

        "completed":
        completed_steps,

        "remaining":
        remaining_steps,

        "percentage":
        percentage
    }


def find_task(
    task_id,
    data
):

    for task in data["tasks"]:

        if (
            task["task_id"] ==
            task_id
        ):
            return task

    return None


def build_completion_report(
    task
):

    total_steps = len(
        task["steps"]
    )

    completed_steps = sum(

        1

        for step
        in task["steps"]

        if step["completed"]
    )

    notes_count = len(
        task["notes"]
    )

    file_count = len(
        task["attachments"]
    )

    percent = task[
        "progress"
    ][
        "percentage"
    ]

    overview = f"""

Task execution completed successfully.

Task:
{task['heading']}

All planned implementation activities
have been completed and validated.

Supporting documentation,
evidence files,
notes,
and execution records
have been successfully archived.

Completion Rate:
{percent}%

This task is now considered
ready for archival,
inheritance,
future reference,
and stewardship review.

""".strip()

    evaluation = {

        "steps_total":
        total_steps,

        "steps_completed":
        completed_steps,

        "completion_percentage":
        percent,

        "notes":
        notes_count,

        "attachments":
        file_count,

        "archive_ready":
        True
    }

    return (
        overview,
        evaluation
  )
  
