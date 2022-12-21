from fastapi import FastAPI


def start_app() -> FastAPI:
    app = FastAPI(title="TweetCo", version="0.0.1")
    return app


app = start_app()
