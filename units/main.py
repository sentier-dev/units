"""Units API."""

import argparse

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from starlette.middleware.cors import CORSMiddleware

from units.routes import router
from units.settings import get_settings


def create_app() -> FastAPI:
    """Create the FastAPI application object
    Returns:
        FastAPI: the application object
    """
    sentry_sdk.init(
        dsn=get_settings().SENTRY_DSN.get_secret_value(),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )
    app.include_router(router)
    app = VersionedFastAPI(app, enable_latest=True, default_version=(0, 1))

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Units API")
    parser.add_argument(
        "-r",
        dest="f_reload",
        action="store_true",
        help="enable auto-reloading",
        default=False,
    )
    args = parser.parse_args()
    uvicorn.run(
        "units.main:create_app",
        reload=args.f_reload,
        host=get_settings().HOST_IP,
    )
