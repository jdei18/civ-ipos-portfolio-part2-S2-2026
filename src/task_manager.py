from src.task import Task
from src.file_handler import save_tasks
from datetime import datetime
from dateutil import parser


def add_task(tasks, title, description, due_date):
    """
    Add a new task to the task list.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the new task.
        description (str): A brief description of the task.
        due_date (str): The due date of the task in 'DD-MM-YYYY' format.

    Returns:
        bool: True if the task is added successfully, False otherwise.

    Raises:
        ValueError: If the due date is not in the correct format.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    # Prevent duplicate tasks
    if any(task.title == title for task in tasks):
        print("Error: A task with this title already exists.")
        return False

    date_first_section = (
        due_date.strip()
        .replace("-", " ")
        .replace("/", " ")
        .replace(".", " ")
        .split()[0]
    )

    #Prevent date with invalid format from being assigned to task
    if len(date_first_section) == 4 and date_first_section.isdigit():
        print("Error: Invalid date format. Use day-month-year order.")
        return False
    
    # Validate due date and format
    try:
        parsed_due_date = parser.parse(due_date, dayfirst=True)
    except ValueError:
        print("Error: Invalid date format. Use day-month-year order.")
        return False

    # Prevent past due date from being assigned to task
    if parsed_due_date.date() < datetime.now().date():
        print("Error: A task with a due date in the past cannot be created.")
        return False
    
    tasks.append(Task(title, description, due_date))
    save_tasks(tasks)
    return True


def delete_task(tasks, title):
    """
    Delete a task from the task list based on its title.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the task to be deleted.

    Returns:
        bool: True if the task was found and deleted, False otherwise.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    for task in tasks:
        if task.title == title:
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False


def list_tasks(tasks, status=None):
    """
    Display tasks in the task list, optionally filtered by status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str, optional): The status to filter tasks
        by (e.g., "pending" or "completed").

    Returns:
        None

    Side Effects:
        - Prints the list of tasks to the console.
    """
    if not status:
        # If status is not set
        filtered = tasks
    else:
        # Filter tasks based on their status
        filtered = []
        for task in tasks:
            if task.status == status:
                filtered.append(task)

    if not filtered:
        print("No tasks found.")
        return
    for task in filtered:
        print(
            f"{task.title} | {task.description} | "
            f"Due: {task.due_date} | Status: {task.status}"
        )


def filter_tasks_by_status(tasks, status):
    """
    Filter tasks by their status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str): The status to filter tasks by (e.g., "pending" or "completed").

    Returns:
        list: A list of Task objects that match the specified status.
    """
    return [task for task in tasks if task.status == status]

def update_overdue_tasks(tasks):
    """
    Update pending tasks to overdue when their due date has passed.

    Args:
        tasks (list): The list of existing Task objects.

    Returns:
        bool: True if any task status was updated, otherwise False.
    """
    updated = False

    for task in tasks:
        parsed_due_date = parser.parse(task.due_date, dayfirst=True)
        
        if (task.status == "pending"
            and parsed_due_date.date() < datetime.now().date()):
            task.status = "overdue"
            updated = True

    if updated:
        save_tasks(tasks)

    return updated