from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import auth, database

from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/")
async def get_all_stones(session=Depends(database.session)) -> list:
    stones = session.query(Stone).all()
    return list(map(lambda x: PydanticStone.from_orm(x), stones))
