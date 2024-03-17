from fastapi import APIRouter, Depends, status
from services.auth import token_interceptor
from models.user import UserViewModel, UserCreateOrUpdateModel
from database import get_db_context
from sqlalchemy.orm import Session
from services import user as user_service
from uuid import UUID
from schemas.user import User
from utilities.utils import http_exception

router = APIRouter(prefix="/users", tags=["User"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_user(
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> list[UserViewModel]:
    """ Get all users
        - If the user is admin -> Get all users in the same company
        - If the usre is non admin -> Get the user from the token (logged user)
    Args:
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Returns:
        list[UserViewModel]: A list of users
    """
    if not user.is_admin:
        return [user_service.get_user_by_id(user.id, db)]
    
    return user_service.get_users_by_company_id(user.company_id, db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    id: UUID,
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> UserViewModel:
    """ Get user by Id
        - TODO: Need to check if user id to get has the same company with the logged user
    Args:
        id (UUID): Id of the user
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 403 Forbbiden in case the user does not have permission to do this action (not admin)
        http_exception: 404 Not found in case the user could not be found

    Returns:
        UserViewModel: A user model
    """
    # Not user admin
    if not user.is_admin and user.id != id:
        raise http_exception(403, "You don't have permission to do this action")
    result = user_service.get_user_by_id(id, db)
    if not result:
        raise http_exception(404, "The user could not be found")
    return result
    

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_a_new_user(model: UserCreateOrUpdateModel, db: Session = Depends(get_db_context))->bool:
    """ Create a new user

    Args:
        model (UserCreateOrUpdateModel): user to create
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found in case the company could not be found
        http_exception: 409 Conflict in case the user_name or email exist
        http_exception: 500 Internal error for the server error

    Returns:
        bool: True if sucess
    """
    result = user_service.create_or_update_user(db, model)
    match result:
        case status.HTTP_201_CREATED:
            return True
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The company does not found")
        case status.HTTP_409_CONFLICT:
            raise http_exception(409, "The email or username already exist")
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There was an error while creating user")
        

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_a_user(
    id: UUID,
    model: UserCreateOrUpdateModel,
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> bool:
    """ Update a user
        - TODO: Need to check if user id to update has the same company with the logged user
    Args:
        id (UUID): Id of the user
        model (UserCreateOrUpdateModel): user model to update
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 403 Forbiden in case user is non admin and try to update for other user
        http_exception: 404 Not found in case the user could not be found to update
        http_exception: 409 Conflict in case the user_name or email exist
        http_exception: 500 Internal server for the server error

    Returns:
        bool: True if success
    """
    if not user.is_admin and user.id != id:
        raise http_exception(403, "You have permission to do this action")
    result = user_service.create_or_update_user(db, model, id)
    match result:
        case status.HTTP_200_OK:
            return True
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The user or the company not found")
        case status.HTTP_409_CONFLICT:
            raise http_exception(409, "The email or username already exist")
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There was an error while creating user")
        

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_user(
    id: UUID,
    user: User = Depends(token_interceptor),
    db: Session = Depends(get_db_context)) -> None:
    """ Soft delete a user
       - TODO: Need to check if user id detele get has the same company with the logged user

    Args:
        id (UUID): User id
        user (User, optional): User from token. Defaults to Depends(token_interceptor).
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 403 Forbiden in case the user does not have permission to do this action (non admin)
        http_exception: 404 Not found in case the user could not be found to delete
        http_exception: 500 Internal error in case internal server error

    Returns:
        _type_: 204 No content
    """
    if not user.is_admin and user.id != id:
        raise http_exception(403, "You don't have permission to do this action")
    result = user_service.delete_a_user(id, db)
    match result:
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The user id does not exist to delete")
        case status.HTTP_204_NO_CONTENT:
            return status.HTTP_204_NO_CONTENT
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There is an error while deleting the user")