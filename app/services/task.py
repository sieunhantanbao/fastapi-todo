from uuid import UUID
from sqlalchemy.orm import Session
from schemas.user import User
from models.task import TaskCreateOrUpdateModel, TaskViewModel
from schemas.task import Task
from fastapi import status
import logging
from datetime import datetime

def get_all_tasks(db: Session) -> list[TaskViewModel]:
    """ Get all tasks

    Args:
        db (Session): Db Context

    Returns:
        list[TaskViewModel]: List of the tasks
    """
    return db.query(Task).all()

def get_task_by_id(id: UUID, user_id: UUID, is_admin: bool, db: Session) -> TaskViewModel:
    """ Get task by Id.
        - If the user is admin, then get the task by the task id
        - If non user admin, then get the task by user_id and task id
        - TODO: Need to check for the case admin to ensure that the task he/she is trying to get belong to the same company.

    Args:
        id (UUID): Id of the task
        user_id (UUID): User id
        is_admin (bool): True/False
        db (Session): Db context

    Returns:
        TaskViewModel: A task view model
    """
    if is_admin:
        return db.query(Task).filter(Task.id==id).first()
    return db.query(Task).filter(Task.id==id, Task.user_id==user_id).first()

def get_tasks_by_user_id(user_id: UUID, db: Session) -> list[TaskViewModel]:
    """ Get Tasks by user_id

    Args:
        user_id (UUID): User id
        db (Session): Db context

    Returns:
        list[TaskViewModel]: A list of tasks
    """
    return db.query(Task).filter(Task.user_id==user_id).all()

def get_tasks_by_user_ids(user_ids: list[UUID], db: Session) -> list[TaskViewModel]:
    """ Get all Tasks by a list of user_ids

    Args:
        user_ids (list[UUID]): List of user_ids
        db (Session): Db context

    Returns:
        list[TaskViewModel]: A list of tasks
    """
    return db.query(Task).filter(Task.user_id.in_(user_ids)).all()

def create_or_update_a_task(user_id: UUID, is_admin: bool, model: TaskCreateOrUpdateModel, db: Session, id: UUID = None) -> status:
    """ Create or update a task

    Args:
        user_id (UUID): User id
        is_admin (bool): Is admin
        model (TaskCreateOrUpdateModel): Create or update task model
        db (Session): Db context
        id (UUID, optional): Id of the task in case of update. Defaults to None.

    Returns:
        status: 201 Created/ 404 Not found/ 403 Forbidden/ 200 Ok
    """
    # Check if the user_id exist
    user_exist = db.query(User).filter(User.id == user_id).first()
    if not user_exist:
        logging.error(f"The user id = {model.user_id} could not be found")
        return status.HTTP_404_NOT_FOUND
    
    if id is None: # Create new
        new_task = Task(**model.model_dump())
        new_task.user_id = user_id
        
        db.add(new_task)
        db.commit()
        return status.HTTP_201_CREATED
    
    existing_task: Task = None
    if not is_admin:
        existing_task = db.query(Task).filter(Task.id==id, Task.user_id == user_id).first()
        if not existing_task:
            logging.error(f"You don't have permission to do this action")
            return status.HTTP_403_FORBIDDEN
    else:    
        existing_task = db.query(Task).filter(Task.id==id).first()
        if not existing_task:
            logging.error(f"The task id = {id} could not be found")
            return status.HTTP_404_NOT_FOUND
    
    existing_task.summary = model.summary
    existing_task.description = model.description
    existing_task.priority = model.priority
    existing_task.status = model.status
    existing_task.user_id = user_id
    existing_task.updated_at = datetime.now()
   
    db.add(existing_task)
    db.commit()
    return status.HTTP_200_OK

def delete_a_task(id: UUID, user_id: UUID, is_admin: bool, db: Session) -> status:
    """ Delete a task

    Args:
        id (UUID): Id of the task
        user_id (UUID): user id
        is_admin (bool): Is admin
        db (Session): Db context

    Returns:
        status: 403 Forbidden/ 404 Not found/ 204 No content
    """
    task_to_delete: Task = None
    if not is_admin:
        task_to_delete = db.query(Task).filter(Task.id==id, Task.user_id == user_id).first()
        if not task_to_delete:
            logging.error(f"You don't have permission to do this action")
            return status.HTTP_403_FORBIDDEN
    else:
        task_to_delete = db.query(Task).filter(Task.id==id).first()
        if not task_to_delete:
            logging.error(f"The task with id = {id} could not found")
            return status.HTTP_404_NOT_FOUND
    
    db.delete(task_to_delete)
    db.commit()
    return status.HTTP_204_NO_CONTENT



