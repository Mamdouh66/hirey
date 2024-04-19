from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_application():
    app = FastAPI(title="Hirey", version="0.1.0") # TODO: Add through config

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()
