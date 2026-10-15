# task

A lightweight stewardship task tracker for documenting, auditing, and inheriting operational work.

## What it includes

- CLI task creation via `add_task.py`
- Step-level progress tracking via `track_task.py`
- Task completion reporting via `complete_task.py`
- Validation script via `validate.py`
- Dynamic dashboard served locally via `server.py`

## Quick start

### 1) Run the dashboard

```bash
python3 server.py
```

Then open:

```text
http://localhost:8000
```

### 2) Create a task from the CLI

```bash
python3 add_task.py "System migration" "Move legacy records into the new archive flow" --steps "Review inventory,Archive files,Validate results"
```

### 3) Mark a step complete

```bash
python3 track_task.py TASK-000001 1
```

### 4) Complete the task

```bash
python3 complete_task.py TASK-000001
```

### 5) Validate the repository state

```bash
python3 validate.py
```

## Notes

- The repository persists task state in `data.json` and registry counters in `registry.json`.
- The dashboard uses a local JSON API served by `server.py` and therefore does not require any external database or framework.
- The `attachments/` directory is created automatically when files are added to tasks.
