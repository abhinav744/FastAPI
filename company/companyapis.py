from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"company_name": "example company, llc"}

@router.get("/employee")
async def number_of_employees():
    return 162