from fastapi import APIRouter
from database import get_all_lectures, get_files

router = APIRouter(
    prefix="/lectures",
    tags=["Lectures"]
)


@router.get("/")
def get_lectures():

    lectures = get_all_lectures()

    response = []

    for lecture in lectures:

        lecture["files"] = get_files(
            lecture["lecture_id"]
        )

        response.append(lecture)

    return response