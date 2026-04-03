"""
Main module of exchange backend.
"""
import logging
import os
import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.testing.route import testing
from app.user.route import user
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
        docs_url="/docs" ,
        redoc_url="/redoc",
        title=' Chain Arbitrage | LOGIN API',
        debug=False
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

    app.include_router(testing, tags=['test'])
    app.include_router(user,tags=['user'])
    app.include_router()
    return app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app)
