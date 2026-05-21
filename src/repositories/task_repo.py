from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.schemas.tasks import TaskStatus
from models.task import Tasks


async def complete_task(db: AsyncSession, task_id: int, matches: list[dict]) -> None:

    if not matches:
        stmt = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .values(
                status=TaskStatus.FAILED,
            )
        )

        await db.execute(stmt)
        await db.commit()
        return

    best_choice_id = matches[0]["job_id"]

    result_json = {
        str(match["job_id"]): match["score"]
        for match in matches
    }

    stmt = (
        update(Tasks)
        .where(Tasks.id == task_id)
        .values(
            status=TaskStatus.COMPLETED,
            best_choice_id=best_choice_id,
            result=result_json,
        )
    )

    await db.execute(stmt)
    await db.commit()