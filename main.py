import os
from contextlib import asynccontextmanager
from typing import Annotated
from datetime import datetime

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Path
from fastapi.responses import FileResponse

from app.dependencies import get_aml_provider
from app.providers import AMLProvider
from app.schemas import CheckAddressRequest, CheckAddressResponse
from app.tasks import generate_report, get_reports_dir, init_reports_dir


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_reports_dir()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/check-address')
async def check_address(
    request: CheckAddressRequest,
    background_tasks: BackgroundTasks,
    provider: Annotated[AMLProvider, Depends(get_aml_provider)],
) -> CheckAddressResponse:
    post_data = dict(hash=request.address, asset=request.currency)
    response = await provider.get_aml_data(post_data)

    data = response.get('data', {})
    status = data.get('status')

    if status == 'pending':
        return CheckAddressResponse(status='pending')

    if status == 'success':
        extras = data.get('extras', {})
        services = extras.get('services', {})
        categories = services.get('malicious_event')

        background_tasks.add_task(
            generate_report,
            report_data=dict(
                datetime=datetime.now(),
                address=request.address,
                currency=request.currency,
                risk_score=data.get('riskscore'),
                risk_level=data.get('risk_score_level'),
                categories=categories,
                file_name=f'{request.currency}{request.address}',
            ),
        )

        return CheckAddressResponse(
            status='success',
            risk_score=data.get('riskscore'),
            risk_level=data.get('risk_score_level'),
            categories=categories,
            pdf_url=f'/report/{request.currency}{request.address}',
        )

    return CheckAddressResponse(status=status or 'unknown')


@app.get('/report/{file_name}')
async def get_report(
    file_name: Annotated[str, Path(pattern=r'^[a-zA-Z0-9]+$')],
) -> FileResponse:
    reports_dir = get_reports_dir()
    if reports_dir is None:
        raise HTTPException(
            status_code=500, detail='Reports directory not initialized'
        )

    file_path = os.path.join(reports_dir, f'{file_name}.pdf')

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail='Report not found')

    return FileResponse(file_path, media_type='application/pdf')
