from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.auth import token_interceptor
from utilities.utils import http_exception
from services import task as task_service, user as user_service
from database import get_db_context
from models.task import TaskCreateOrUpdateModel, TaskViewModel
from schemas.user import User


router = APIRouter(prefix="/tasks", tags=["Task"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ) -> list[TaskViewModel]:
    """ Get all tasks. If the user is admin, then get all tasks in a company else get all tasks belong to the user

    Args:
        db (Session, optional): Db context. Defaults to Depends(get_db_context).
        user (User, optional): User from token. Defaults to Depends(token_interceptor).

    Returns:
        list[TaskViewModel]: List of the tasks
    """
    if user.is_admin:
        users_in_company = user_service.get_users_by_company_id(user.company_id, db)
        user_ids = [user.id for user in users_in_company]
        return task_service.get_tasks_by_user_ids(user_ids, db)
    return task_service.get_tasks_by_user_id(user.id, db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(
    id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ) -> TaskViewModel:
    """ Get a task by Id
        - If the user is admin, then get the task by the task id
        - If non user admin, then get the task by user_id and task id

    Args:
        id (UUID): Task Id
        db (Session, optional): Db context. Defaults to Depends(get_db_context).
        user (User, optional): User. Defaults to Depends(token_interceptor).

    Returns:
        TaskViewModel: A Task view model
    """
    return task_service.get_task_by_id(id, user.id, user.is_admin, db)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_a_task(
    model: TaskCreateOrUpdateModel,
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> bool:
    """ Create a task

    Args:
        model (TaskCreateOrUpdateModel): Task model to create
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found in case the user id could not be found

    Returns:
        bool: True if task created successfully
    """
    result = task_service.create_or_update_a_task(user.id, user.is_admin, model, db)
    match result:
        case status.HTTP_201_CREATED:
            return True
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The user could not be found")
        
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_a_task(
    id: UUID,
    model: TaskCreateOrUpdateModel,
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> bool:
    """ Update a task

    Args:
        id (UUID): Id of the task
        model (TaskCreateOrUpdateModel): Task model to update
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found in case the user id could not be found
        http_exception: 403 Forbidden in cas the user does not have permission to do this action

    Returns:
        bool: _description_
    """
    result = task_service.create_or_update_a_task(user.id, user.is_admin, model, db, id)
    match result:
        case status.HTTP_200_OK:
            return True
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The user could not be found")
        case status.HTTP_403_FORBIDDEN:
            raise http_exception(403, "You don't have permission to perform this action")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_task(
    id: UUID, 
    user: User = Depends(token_interceptor), 
    db: Session = Depends(get_db_context)) -> None:
    """ Delete a task

    Args:
        id (UUID): Task Id to delete
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found in case the task could not be found to delete
        http_exception: 403 Forbidden in case the user does not have permission to do this action

    Returns:
        _type_: 204 No content
    """
    result = task_service.delete_a_task(id, user.id, user.is_admin, db)
    match result:
        case status.HTTP_204_NO_CONTENT:
            return status.HTTP_204_NO_CONTENT
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The task could not be found to delete")
        case status.HTTP_403_FORBIDDEN:
            raise http_exception(403, "You don't have permission to do this action")
            

