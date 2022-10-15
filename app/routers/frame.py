from fastapi import APIRouter, Depends, HTTPException, status

from app.database.models.frame import Frame, PydanticFrame
from app.dependencies import auth, database
from model.inference import get_results

from pydantic import ValidationError

router = APIRouter()


@router.get("/all/")
async def get_all_frames(session=Depends(database.session)) -> list:
    frames = session.query(Frame).all()
    return list(map(lambda x: PydanticFrame.from_orm(x), frames))


@router.get("/{frame_id}")
async def get_singe_frame_data(frame_id: int, session=Depends(database.session)) -> PydanticFrame:
    return Frame.get_by_frame_id(session, frame_id)

@router.get("/video/")
async def get_video_stream(session=Depends(database.session)):
    for i in get_results('video.mp4'):
        print(i)

