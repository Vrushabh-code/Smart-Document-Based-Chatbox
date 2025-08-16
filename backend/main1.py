# # 📁 File: main1.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from endpoint import router as api_router

# app = FastAPI(
#     title="FinanceBot API",
#     description="An API for generating equity research reports from PDF documents using Gemini and LangChain.",
#     version="1.0.0"
# )

# # ✅ CORS configuration (for local React frontend or other tools like Postman)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8080"],  # You can restrict this to ["http://localhost:3000"] if React is local
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Route mount
# app.include_router(api_router, prefix="/api")

# # ✅ Health check/root endpoint
# @app.get("/")
# async def root():
#     return {
#         "message": "✅ FinanceBot API is running.",
#         "docs": "Visit /docs for Swagger UI.",
#         "api_base": "/api"
#     }
    # main1.py code:-
# 📁 File: main1.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint import router as api_router

app = FastAPI(
    title="FinanceBot API",
    description="An API for generating equity research reports from PDF documents using Gemini and LangChain.",
    version="1.0.0"
)

# ✅ CORS configuration (for local React frontend or other tools like Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http://localhost:3000"],  # You can restrict this to ["http://localhost:3000"] if React is local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route mount
app.include_router(api_router, prefix="/api")

# ✅ Health check/root endpoint
@app.get("/")
async def root():
    return {
        "message": "✅ FinanceBot API is running.",
        "docs": "Visit /docs for Swagger UI.",
        "api_base": "/api"
    }
