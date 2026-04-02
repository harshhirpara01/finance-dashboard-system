import json
import requests
from fastapi.responses import JSONResponse

HEM_INTERNAL_SERVER_ERROR = "Something went wrong. Please try again."



HSM_SUCCESS = "success"
HEM_ERROR = "error"

def successResponse(status_code, msg, data={}):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": msg,
            "data": data,
        }
    )


def errorResponse(status_code, msg, data={}):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": msg,
            "data": data,
        }
    )

