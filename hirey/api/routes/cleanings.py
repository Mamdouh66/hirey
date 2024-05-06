from typing import List

from fastapi import APIRouter, Body, Depends, status, HTTPException

from hirey.models.cleaning import CleaningCreate, CleaningPublic
from hirey.db.repositories.cleanings import CleaningsRepository
from hirey.api.dependencies.database import get_repository


router = APIRouter()


@router.get(
    "/{id}/", response_model=CleaningPublic, name="cleanings:get-cleaning-by-id"
)
async def get_cleaning_by_id(
    id: int,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)

    if not cleaning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )

    return cleaning


@router.get(
    "/",
    response_model=List[CleaningPublic],
    name="cleanings:get-all-cleanings",
)
async def get_all_cleanings(
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningPublic]:
    return await cleanings_repo.get_all_cleanings()


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create-cleaning",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)

    return created_cleaning
