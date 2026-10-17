import click
from src.task_manager import (
    add_task,
    delete_task,
    list_tasks,
    update_overdue_tasks,
    filter_tasks_by_status
)
from src.file_handler import load_tasks


@click.group()
def cli():
    """
    Task Manager CLI.

    Commands:

    add
        Add a new task.

        --title
            The name of the task.

        --description
            A description of the task. (optional)

        --due-date
            The task due date (day-month-year).

    delete
        Delete an existing task using its title.

        --title
            The title of the task to delete.

    list
        Display saved tasks.

        --status
            Optionally filter tasks by status.

    PowerShell shortcut:

        function tm { python main.py @args }

    This allows commands such as:

        tm list
        tm add --title "Task" --due-date "08-07-2027"
    """
    pass


@cli.command()
@click.option("--title", required=True)
@click.option("--description", default="")
@click.option("--due-date", required=True)
def add(title, description, due_date):
    """Add a new task."""
    tasks = load_tasks()
    update_overdue_tasks(tasks)
    add_task(tasks, title, description, due_date)


@cli.command()
@click.option("--title", required=True)
def delete(title):
    """Delete a task."""
    tasks = load_tasks()
    update_overdue_tasks(tasks)

    if delete_task(tasks, title):
        click.echo("Task deleted successfully.")
    else:
        click.echo("Task not found.")


@cli.command()
@click.option("--status", required=False)
def list(status):
    """List tasks, optionally filtered by status."""
    tasks = load_tasks()
    update_overdue_tasks(tasks)

    if status:
        tasks = filter_tasks_by_status(tasks, status)

    list_tasks(tasks)


if __name__ == "__main__":
    cli()
