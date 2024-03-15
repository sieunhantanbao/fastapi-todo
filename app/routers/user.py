from fastapi import APIRouter, Depends, status
from models.user import UserViewModel, UserCreateOrUpdateModel
from database import get_db_context
from sqlalchemy.orm import Session
from services import user as user_service
from uuid import UUID
from utilities.utils import http_exception

router = APIRouter(prefix="/users", tags=["User"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_user(db: Session = Depends(get_db_context)) -> list[UserViewModel]:
    """ Get all users

    Args:
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Returns:
        list[UserViewModel]: List of users
    """
    return user_service.get_all_users(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(id: UUID, db: Session = Depends(get_db_context)) -> UserViewModel:
    """ Get user by id

    Args:
        id (UUID): Id of the user
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 error if the user could not be founs

    Returns:
        UserViewModel: A user view model
    """
    result = user_service.get_user_by_id(id, db)
    if not result:
        raise http_exception(404, "The user could not be found")
    return result

@router.get("/company/{company_id}", status_code=status.HTTP_200_OK)
async def get_users_by_company_id(company_id: UUID, db:Session = Depends(get_db_context)) -> list[UserViewModel]:
    """ Get all users by company id

    Args:
        company_id (UUID): Company Id
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Returns:
        list[UserViewModel]: A list of user models
    """
    return user_service.get_users_by_company_id(company_id, db)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_a_new_user(model: UserCreateOrUpdateModel, db: Session = Depends(get_db_context))->bool:
    """ Create a new user

    Args:
        model (UserCreateOrUpdateModel): user to create
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found
        http_exception: 409 Conflict
        http_exception: 500 Internal error

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
async def update_a_user(id: UUID, model: UserCreateOrUpdateModel, db: Session = Depends(get_db_context)) -> bool:
    """ Update a user

    Args:
        id (UUID): User id to update
        model (UserCreateOrUpdateModel): User model to update
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found
        http_exception: 500 Internal error

    Returns:
        _type_: True if success
    """
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
async def delete_a_user(id: UUID, db: Session = Depends(get_db_context)) -> None:
    """ Delete a user by Id

    Args:
        id (UUID): Id of the user
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 Not found
        http_exception: 500 Internal error

    Returns:
        _type_: _description_
    """
    result = user_service.delete_a_user(id, db)
    match result:
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The user id does not exist to delete")
        case status.HTTP_204_NO_CONTENT:
            return status.HTTP_204_NO_CONTENT
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There is an error while deleting the user")