from datetime import datetime
from models.company import CompapnyViewModel, CompanyCreateOrUpdateModel
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas.company import Company
from uuid import UUID

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

def create_or_update_company(model: CompanyCreateOrUpdateModel,  db: Session, company_id: UUID = None) -> bool:
    """ Create or update an company

    Args:
        model (CompanyCreateOrUpdateModel): createOrUpdateModel
        db (Session): Db context
        company_id (UUID, Optional): Company Id to update
    Returns:
        bool: True if success else False
    """
    try:
        if company_id is None: # Create new
            new_company = Company(**model.model_dump())
            
            db.add(new_company)
            db.commit()
            return True
        else: # Update
            existing_company = db.query(Company).filter(Company.id==company_id).first()
            
            if not existing_company:
                print(f"The company you are trying to update does not exist. CompanyId = {company_id}")
                return False
            
            existing_company.name = model.name
            existing_company.description = model.description
            existing_company.rating = model.rating
            existing_company.updated_at = datetime.now()
            db.add(existing_company)
            db.commit()
            
            return True
    except Exception as e:
        print(e)
        return False
    
def delete_a_company(id: UUID, db:Session) -> bool:
    """ Delete a company

    Args:
        id (UUID): Id of the company to delete
        db (Session): Db context

    Returns:
        bool: True if success else False
    """
    try:
        company_to_delete = db.query(Company).filter(Company.id == id).first()
        if not company_to_delete:
            print("The company does not found")
            return False
        
        db.delete(company_to_delete)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False