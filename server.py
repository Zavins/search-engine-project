import uvicorn
from search import load, unload

if __name__ == "__main__":
    load()
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        access_log=True,
        use_colors=True,
        proxy_headers=True,
    )
    unload()
