from uuid import UUID
from fastapi import APIRouter, status, Depends
from utilities.utils import http_exception
from services import company as company_service
from models.company import CompanyCreateOrUpdateModel, CompapnyViewModel
from sqlalchemy.orm import Session
from database import get_db_context


router = APIRouter(prefix="/companies", tags=["Company"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_companies(db: Session = Depends(get_db_context)) -> list[CompapnyViewModel]:
    """ Get all companies

    Args:
        db (Session, optional): Db conext. Defaults to Depends(get_db_context).

    Returns:
        list[CompapnyViewModel]: List of companies
    """
    return company_service.get_all_company(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_company_by_id(id: UUID, db: Session = Depends(get_db_context))-> CompapnyViewModel:
    """ Get comanpy by Id

    Args:
        id (UUID): Id of the company
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 error

    Returns:
        CompapnyViewModel: Company model
    """
    company = company_service.get_company_by_id(id, db)
    if not company:
        raise http_exception(404, "Company not found")
    return company

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_company(model: CompanyCreateOrUpdateModel, db: Session = Depends(get_db_context)) -> bool:
    """ Create a new Company

    Args:
        model (CompanyCreateOrUpdateModel): Company to create
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 500 internal error

    Returns:
        bool: True if success else False
    """
    result = company_service.create_or_update_company(model, db)
    match result:
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There was an error while creating Company")
        case status.HTTP_201_CREATED:
            return True

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def create_new_company(id: UUID, model: CompanyCreateOrUpdateModel, db: Session = Depends(get_db_context)) -> bool:
    """ Update a company

    Args:
        id (UUID): Company Id to update
        model (CompanyCreateOrUpdateModel): Company to edit
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 500 internal error

    Returns:
        bool: True if success else False
    """
    result = company_service.create_or_update_company(model, db, id)
    match result:
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The company could not be found to update")
        case status.HTTP_200_OK:
            return True
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "There was an error while updating Company")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_copany(id: UUID, db: Session = Depends(get_db_context)) -> None:
    """ Delete a company

    Args:
        id (UUID): Id of the company to delete
        db (Session, optional): Db context. Defaults to Depends(get_db_context).

    Raises:
        http_exception: 404 error if the company could not be found to delete

    Returns:
        bool: True if success else False
    """
    result = company_service.delete_a_company(id, db)
    match result:
        case status.HTTP_204_NO_CONTENT:
            return status.HTTP_204_NO_CONTENT
        case status.HTTP_404_NOT_FOUND:
            raise http_exception(404, "The company not found")
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise http_exception(500, "Unable to delete this company")