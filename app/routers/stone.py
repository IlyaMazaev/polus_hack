from fastapi import APIRouter, Depends, HTTPException, status

from app.database.models.stone import Stone, PydanticStone
from app.dependencies import auth, database

from pydantic import ValidationError

router = APIRouter()


@router.get("/all/")
async def get_all_stones(session=Depends(database.session)):
    stones = session.query(Stone).all()
    return list(map(lambda x: PydanticStone.from_orm(x), stones))
