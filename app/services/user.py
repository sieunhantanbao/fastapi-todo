from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from schemas.user import User, get_hashed_password
from schemas.company import Company
from models.user import UserViewModel, UserCreateOrUpdateModel
from datetime import datetime
from fastapi import status
import logging

def get_all_users(db:Session) -> list[UserViewModel]:
    """ Get all users

    Args:
        db (Session): Db context

    Returns:
        list[UserViewModel]: List of users to return
    """
    return db.query(User).all()

def get_user_by_id(id:UUID, db:Session) -> UserViewModel:
    """ Get a user by Id

    Args:
        id (UUID): User Id to get
        db (Session): Db context

    Returns:
        UserViewModel: A single user object to return
    """
    return db.query(User).filter(User.id==id).first()

def get_users_by_company_id(company_id, db: Session) -> list[UserViewModel]:
    """ Get all users by company Id

    Args:
        company_id (_type_): Id of the company
        db (Session): Db context

    Returns:
        list[UserViewModel]: A list of user model to return
    """
    return db.query(User).filter(User.company_id==company_id).all()

def create_or_update_user(db: Session, model: UserCreateOrUpdateModel, id: UUID = None) -> status:
    """ Create or update user

    Args:
        db (Session): Db context
        model (UserCreateOrUpdateModel): User model to create or update
        id (UUID, optional): Id of the user id to update. Defaults to None.

    Returns:
        status: Http Status code
    """
    try:
        # Check if Company exist
        company_exist = db.query(Company).filter(Company.id == model.company_id).first()
        if not company_exist:
            logging.error(f"The company id={model.company_id} could not be found")
            return status.HTTP_404_NOT_FOUND
        
        if id is None: # Create new
            # To resolve the issue: 'password' is an invalid keyword argument for User
            password = model.password
            user_model = model.model_dump()
            del user_model['password']
            # Check if the email AND/OR username exist in database
            user_exist = db.query(User).filter(or_(User.email==model.email, User.user_name == model.user_name)).first()
            if user_exist:
                logging.error("The user_name or email have been existed")
                return status.HTTP_409_CONFLICT
            new_user = User(**user_model)
            new_user.hashed_password = get_hashed_password(password)
            
            db.add(new_user)
            db.commit()
            return status.HTTP_201_CREATED
        else: # Update
            existing_user = db.query(User).filter(User.id==id).first()
            if not existing_user:
                return status.HTTP_404_NOT_FOUND
            # Check if the email AND/OR username exist in database
            if existing_user.email != model.email:
                user_exist = db.query(User).filter(User.email==model.email).first()
                if user_exist:
                    logging.error(f"The email={model.email} exists")
                    return status.HTTP_409_CONFLICT
            elif existing_user.user_name != model.user_name:
                user_exist = db.query(User).filter(User.user_name == model.user_name).first()
                if user_exist:
                    logging.error(f"The user_name={model.user_name} exists")
                    return status.HTTP_409_CONFLICT
            existing_user.user_name = model.user_name
            existing_user.first_name = model.first_name
            existing_user.last_name = model.last_name
            existing_user.email = model.email
            existing_user.is_active = model.is_active
            existing_user.is_admin= model.is_admin
            existing_user.updated_at = datetime.now()
            # TODO: We should have a new endpoint/method to change the user password
            if model.password is not None and model.password != '':
                existing_user.hashed_password = get_hashed_password(model.password)
            
            db.add(existing_user)
            db.commit()
            return status.HTTP_200_OK
    except Exception as e:
        logging.error(f"There is an error while creating or update user. {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
def delete_a_user(id: UUID, db: Session) -> status:
    """ Delete a user

    Args:
        id (UUID): User Id to delete
        db (Session): Db context

    Returns:
        bool: True if sucess else False
    """
    user_to_delete = db.query(User).filter(User.id==id).first()
    if not user_to_delete:
        logging.error("The user does not exist to delete")
        return status.HTTP_404_NOT_FOUND
    db.delete(user_to_delete)
    db.commit()
    return status.HTTP_204_NO_CONTENT
        