from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import weather, chat, risk, alerts

app = FastAPI(
    title="WeatherGPT API — SIH26068",
    description="Conversational AI for Weather Forecasting, Alerts, and Climate Information",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)
app.include_router(chat.router)
app.include_router(risk.router)
app.include_router(alerts.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "WeatherGPT API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
