from datetime import datetime
from models.company import CompapnyViewModel, CompanyCreateOrUpdateModel
from sqlalchemy.orm import Session
from fastapi import Depends, status
from schemas.company import Company
from uuid import UUID
import logging

def get_all_company(db: Session) -> list[CompapnyViewModel]:
    """ Get all companies

    Args:
        db (Session): Db context

    Returns:
        list[CompapnyViewModel]: List of CompanyViewModel
    """
    return db.query(Company).all()


def get_company_by_id(id: UUID, db: Session) -> CompapnyViewModel:
    """ Get company by Id

    Args:
        id (UUID): Id of the company
        db (Session): Db context

    Returns:
        CompapnyViewModel: Object CompapnyViewModel
    """
    return db.query(Company).filter(Company.id == id).first()

def create_or_update_company(model: CompanyCreateOrUpdateModel,  db: Session, company_id: UUID = None) -> status:
    """ Create or update an company

    Args:
        model (CompanyCreateOrUpdateModel): createOrUpdateModel
        db (Session): Db context
        company_id (UUID, Optional): Company Id to update
    Returns:
        status: 201 Created/ 404 Not found/ 200 OK/ 500 Internal Server Error
    """
    try:
        if company_id is None: # Create new
            new_company = Company(**model.model_dump())
            
            db.add(new_company)
            db.commit()
            return status.HTTP_201_CREATED
        else: # Update
            existing_company = db.query(Company).filter(Company.id==company_id).first()
            
            if not existing_company:
                logging.error(f"The company you are trying to update does not exist. CompanyId = {company_id}")
                return status.HTTP_404_NOT_FOUND
            
            existing_company.name = model.name
            existing_company.description = model.description
            existing_company.rating = model.rating
            existing_company.updated_at = datetime.now()
            db.add(existing_company)
            db.commit()
            
            return status.HTTP_200_OK
    except Exception as e:
        logging.error(f"There is an error while creating or updating the company. {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
def delete_a_company(id: UUID, db:Session) -> status:
    """ Delete a company

    Args:
        id (UUID): Id of the company to delete
        db (Session): Db context

    Returns:
        status: 204 No content/ 404 Not found/ 500 Internal Server Error
    """
    try:
        company_to_delete = db.query(Company).filter(Company.id == id).first()
        if not company_to_delete:
            logging.error(f"The company id= {id} does not found to delete")
            return status.HTTP_404_NOT_FOUND
        
        db.delete(company_to_delete)
        db.commit()
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        logging.error(f"There is an error while deleting the company with id={id}. {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR