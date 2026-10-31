from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas

from database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# CREATE TASK
@router.post("/", response_model=schemas.TaskResponse,
             status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate,
                db: Session = Depends(get_db)):

    return crud.create_task(db, task)


# GET ALL TASKS
@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):

    return crud.get_all_tasks(db)


# GET TASK BY ID
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = crud.get_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# UPDATE TASK
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int,
                task: schemas.TaskUpdate,
                db: Session = Depends(get_db)):

    updated_task = crud.update_task(db, task_id, task)

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    deleted_task = crud.delete_task(db, task_id)

    if not deleted_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully",
        "task_id": task_id
    }


# MARK TASK AS COMPLETED
@router.patch("/{task_id}/complete",
              response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):

    task = crud.get_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = True

    db.commit()
    db.refresh(task)

    return task


# FILTER TASKS
@router.get("/filter/{filter_type}",
            response_model=list[schemas.TaskResponse])
def filter_tasks(filter_type: str,
                 db: Session = Depends(get_db)):

    if filter_type == "all":
        return crud.get_all_tasks(db)

    elif filter_type == "completed":
        return db.query(crud.Task).filter(
            crud.Task.completed == True
        ).all()

    elif filter_type == "pending":
        return db.query(crud.Task).filter(
            crud.Task.completed == False
        ).all()

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid filter. Use all, completed or pending"
        )
        
        
        