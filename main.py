"""
Main module of exchange backend.
"""
import logging
import os
import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.user.route import user
from app.financial_records.route import records
from app.dashboard.route import dashboard
from common.customized_log import CustomizeLogger
from shared.db import Base, engine

"""
code for save logs in customise path
"""
logger = logging.getLogger(__name__)
module_path = str(pathlib.Path(__file__).parent.absolute())
config_path = str(os.path.join(module_path, "config", "logging_config.json"))
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        title="Finance Dashboard API",
        description=(
            "REST API for user management, financial records, and dashboard summaries. "
            "Use **Authorize** in Swagger UI with `Bearer <access_token>` after logging in."
        ),
        version="1.0.0",
        debug=False,
    )

    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user,tags=['user'])
    app.include_router(records,tags=['financial_records'])
    app.include_router(dashboard,tags=['dashboard-summary'])
    return app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app)
