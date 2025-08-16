# # 📁 File: api/endpoint.py
# from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
# from fastapi.responses import StreamingResponse
# from typing import List, Dict, Optional
# from pydantic import BaseModel
# from io import BytesIO
# import base64
# from f import FinanceBot
# from fastapi import BackgroundTasks 
# import os


# from rag_pipeline import convert_units, format_sources_for_display 
# router = APIRouter()

# # Dependency to get FinanceBot instance per request
# def get_finance_bot():
#     return FinanceBot()

# class ModifyRequest(BaseModel):
#     section: str
#     prompt: str

# class UnitConversionRequest(BaseModel):
#     conversion_profile: str
#     custom_mappings: Optional[Dict[str, str]] = None

# class ElaborateThesisPointRequest(BaseModel):
#     point: str
#     word_count: int = 200

# @router.post("/upload-pdfs")
# async def upload_pdfs(
#     files: List[UploadFile] = File(...),
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     try:
#         # ✅ Create file buffers with .name attribute
#         file_data = []
#         for file in files:
#             content = await file.read()
#             buffer = BytesIO(content)
#             buffer.name = file.filename  # 👈 this is the key fix
#             file_data.append((file.filename, buffer))

#         file_names = [file.filename for file in files]
#         result = bot.analyze_documents([f[1] for f in file_data], file_names)

#         if result["status"] == "error":
#             raise HTTPException(status_code=400, detail=result["errors"])

#         return {
#             "status": "success",
#             "filenames": file_names,
#             "company_name": result["company_name"],
#             "business_overview": result["business_overview"],
#             "quarterly_highlights": result["quarterly_highlights"],
#             "investment_thesis": result["investment_thesis"],
#             "key_thesis_points": result["key_thesis_points"],
#             "pdf_base64": result["pdf_bytes"],
#             "references": result["references"],
#             "detected_units": result["detected_units"]
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")


# @router.post("/modify-report")
# async def modify_report(
#     request: ModifyRequest,
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     """
#     Modify a specific report section based on user prompt.
#     """
#     try:
#         result = bot.modify_report(request.section, request.prompt)
        
#         if result["status"] == "error":
#             raise HTTPException(status_code=400, detail=result["errors"])
        
#         return {
#             "status": "success",
#             "section": request.section,
#             "modified_text": result["modified_section"],
#             "sources": result["sources"],
#             "pdf_base64": result["pdf_bytes"],
#             "key_thesis_points": result.get("key_thesis_points", []),
#             "detected_units": result["detected_units"]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error modifying report: {str(e)}")

# @router.post("/convert-units")
# async def convert_units_endpoint(
#     request: UnitConversionRequest,
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     """
#     Apply unit conversion to report sections.
#     """
#     try:
#         result = bot.apply_unit_conversion(request.conversion_profile, request.custom_mappings)
        
#         if result["status"] == "error":
#             raise HTTPException(status_code=400, detail=result["errors"])
        
#         return {
#             "status": "success",
#             "business_overview": result["business_overview"],
#             "quarterly_highlights": result["quarterly_highlights"],
#             "investment_thesis": result["investment_thesis"],
#             "pdf_base64": result["pdf_bytes"],
#             "detected_units": result["detected_units"]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error applying unit conversion: {str(e)}")

# @router.post("/elaborate-thesis-point")
# async def elaborate_thesis_point(
#     request: ElaborateThesisPointRequest,
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     """
#     Elaborate on a specific investment thesis point.
#     """
#     try:
#         result = bot.elaborate_thesis_point(request.point, request.word_count)
        
#         if result["status"] == "error":
#             raise HTTPException(status_code=400, detail=result["errors"])
        
#         return {
#             "status": "success",
#             "detailed_point": result["detailed_point"],
#             "sources": result["sources"]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error elaborating thesis point: {str(e)}")

# @router.get("/generate-pdf")
# async def generate_pdf(
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     """
#     Return the generated PDF as base64.
#     """
#     try:
#         # Safety check
#         if not hasattr(bot, "pdf_generated_bytes") or bot.pdf_generated_bytes is None:
#             raise HTTPException(
#                 status_code=400,
#                 detail="⚠️ No PDF available. Please upload and analyze documents first using /api/upload-pdfs."
#             )

#         return {
#             "status": "success",
#             "pdf_base64": base64.b64encode(bot.pdf_generated_bytes.getvalue()).decode('utf-8'),
#             "filename": f"{bot.company_name}.pdf"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


# @router.get("/key-thesis-points")
# async def get_key_thesis_points(
#     bot: FinanceBot = Depends(get_finance_bot)
# ):
#     """
#     Retrieve key investment thesis points.
#     """
#     try:
#         if not bot.vectordb or not bot.company_name:
#             raise HTTPException(status_code=400, detail="Please analyze documents first.")
        
#         return {
#             "status": "success",
#             "key_thesis_points": bot.key_thesis_points
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving key thesis points: {str(e)}") 

####################################################################################################################################

# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
# from fastapi.responses import StreamingResponse
# from typing import List, Dict, Optional
# from pydantic import BaseModel, Field
# from io import BytesIO
# import base64
# import uuid
# from f import FinanceBot
# from rag_pipeline import convert_units, elaborate_on_thesis_point, format_sources_for_display, generate_styled_pdf
# import os
# import json
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")    

# router = APIRouter()

# # 📁 In-memory session-like storage
# session_store = {
#     "pdf_bytes": None,
#     "company_name": "Report",
#     "uploaded_files": None
# }

# # 🧰 In-memory stores
# analyze_task_store = {}       # task_id -> result dict
# analyze_task_status = {}      # task_id -> "pending" / "done" / "error"
# bot_store = {}                # task_id -> FinanceBot instance

# # 📦 Request Models
# class ModifyRequest(BaseModel):
#     section: str
#     user_prompt: str

# class UnitConversionRequest(BaseModel):
#     conversion_profile: str
#     custom_mappings: Optional[Dict[str, str]] = None

# class ElaborateThesisPointRequest(BaseModel):
#     point_summary: str
#     word_count: int = 200

# class ThesisEditRequest(BaseModel):
#     index: int
#     action: str  # 'delete', 'rewrite'
#     prompt: Optional[str] = None

# class AddThesisRequest(BaseModel):
#     prompt: str
#     # word_count: int = 150

# class AdjustThesisRequest(BaseModel):
#     index: int
#     direction: str  # 'increase' or 'decrease'

# class ChatRequest(BaseModel): 
#     session_id: str = Field(..., description="Unique session identifier")
#     files: List[str] = Field(..., description="List of filenames to chat with")
#     query: str = Field(..., description="User's query or question")
#     history: str = Field(default="[]", description="JSON string of chat history as list of {'role': 'user'|'assistant', 'content': str}")

# # 🤔 Background Task
# def analyze_background(task_id: str, file_tuples: List[tuple]):
#     bot = FinanceBot(session_id=task_id)
#     try:
#         file_objs = [f[1] for f in file_tuples]
#         file_names = [f[0] for f in file_tuples]
#         result = bot.analyze_documents(file_objs, file_names)

#         analyze_task_store[task_id] = result
#         analyze_task_status[task_id] = "done"
#         bot_store[task_id] = bot

#         session_store["pdf_bytes"] = result["pdf_bytes"]
#         session_store["company_name"] = result["company_name"]
#     except Exception as e:
#         analyze_task_store[task_id] = {"status": "error", "errors": [str(e)]}
#         analyze_task_status[task_id] = "error"

# # 📄 Upload PDFs
# @router.post("/upload-files")
# async def upload_files(files: List[UploadFile] = File(...)):
#     try:
#         uploaded = []
#         for file in files:
#             content = await file.read()
#             buffer = BytesIO(content)
#             buffer.name = file.filename
#             uploaded.append((file.filename, buffer))
#         session_store["uploaded_files"] = uploaded
#         return {"status": "success", "filenames": [f[0] for f in uploaded]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

# # @router.get("/upload-files")
# # async def get_uploaded_filenames():
# #     try:
# #         uploaded_files = session_store.get("uploaded_files", [])
# #         return {"status": "success", "filenames": [f[0] for f in uploaded_files]}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error retrieving filenames: {str(e)}")

# # 📄 Get PDF by filename
# @router.get("/get-pdf/{filename}")
# async def get_pdf(filename: str):
#     try:
#         uploaded_files = session_store.get("uploaded_files", [])
#         for file_name, file_buffer in uploaded_files:
#             if file_name == filename:
#                 file_buffer.seek(0)
#                 return StreamingResponse(
#                     file_buffer,
#                     media_type="application/pdf",
#                     headers={"Content-Disposition": f"inline; filename={filename}"}
#                 )
#         raise HTTPException(status_code=404, detail=f"PDF {filename} not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")

# # 🤜 Trigger Analysis
# @router.post("/analyze")
# async def analyze_async(background_tasks: BackgroundTasks):
#     try:
#         if not session_store.get("uploaded_files"):
#             raise HTTPException(status_code=400, detail="No files uploaded")

#         task_id = str(uuid.uuid4())
#         analyze_task_status[task_id] = "pending"
#         background_tasks.add_task(analyze_background, task_id, session_store["uploaded_files"])

#         return {"status": "processing", "task_id": task_id}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error starting analysis: {str(e)}")

# # 🔎 Check Status
# @router.get("/status/{task_id}")
# async def check_status(task_id: str):
#     status = analyze_task_status.get(task_id)
#     if not status:
#         raise HTTPException(status_code=404, detail="Task ID not found")
#     return {"status": status}

# # 📂 Get Result
# @router.get("/result/{task_id}")
# async def get_result(task_id: str):
#     result = analyze_task_store.get(task_id)
#     if result is None:
#         raise HTTPException(status_code=404, detail="Result not found")
#     return result

# # # 📄 PDF Download
# # @router.get("/generate-pdf")
# # async def generate_pdf():
# #     try:
# #         if not session_store["pdf_bytes"]:
# #             raise HTTPException(status_code=400, detail="PDF not available.")
# #         return StreamingResponse(
# #             session_store["pdf_bytes"],
# #             media_type="application/pdf",
# #             headers={"Content-Disposition": f"inline; filename={session_store['company_name']}.pdf"}
# #         )
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")

# # 📄 PDF Download
# @router.get("/generate-pdf/{task_id}") 
# async def generate_pdf(task_id: str):
#     # Retrieve the specific bot instance for this task
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Analysis session not found.")

#     # Check if the PDF object exists on the bot instance
#     if not bot.pdf_generated_bytes:
#         raise HTTPException(status_code=400, detail="PDF has not been generated for this session.")

#     try:
#         # Get the raw BytesIO object
#         pdf_buffer = bot.pdf_generated_bytes
#         # IMPORTANT: Rewind the buffer to the beginning before reading
#         pdf_buffer.seek(0)

#         company_name = bot.company_name or "report"

#         # Stream the raw binary data
#         return StreamingResponse(
#             pdf_buffer,
#             media_type="application/pdf",
#             headers={"Content-Disposition": f"inline; filename={company_name}.pdf"}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")
# # # 🖊️ Modify Report
# # @router.post("/modify-report/{task_id}")
# # async def modify_report(task_id: str, request: ModifyRequest):
# #     bot = bot_store.get(task_id)
# #     if not bot:
# #         raise HTTPException(status_code=404, detail="Bot not found")
# #     result = bot.modify_report(request.section, request.user_prompt)
# #     if result["status"] == "error":
# #         raise HTTPException(status_code=400, detail=result["errors"])
# #     return {
# #         "status": "success",
# #         "section": request.section,
# #         "modified_text": result["modified_section"],
# #         "sources": result["sources"],
# #         "pdf_base64": result["pdf_bytes"],
# #         "key_thesis_points": result.get("key_thesis_points", []),
# #         "detected_units": result["detected_units"]
# #     }
# @router.post("/modify-report/{task_id}")
# async def modify_report(task_id: str, request: ModifyRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")

#     modified_text, sources, error = bot.modify_report(
#         request.section, request.user_prompt
#     )

#     if error:
#         return {
#             "status": "warning",
#             "message": error,  # Show warning if data not found
#             "modified_text": modified_text,
#             "sources": [],
#             "pdf_base64": None
#         }

#     # Regenerate PDF
#     pdf_bytes, pdf_error = generate_styled_pdf(
#         bot.company_name,
#         bot.llm_business_overview,
#         bot.llm_quarterly_highlights,
#         bot.llm_investment_thesis,
#     )

#     pdf_base64 = (
#         base64.b64encode(pdf_bytes.getvalue()).decode("utf-8")
#         if pdf_bytes else None
#     )

#     return {
#         "status": "success",
#         "message": "Report section modified successfully.",
#         "modified_text": modified_text,
#         "sources": format_sources_for_display(sources),
#         "pdf_base64": pdf_base64,
#         "error": pdf_error
#     }


# # 💚 Edit Thesis
# @router.post("/edit-thesis/{task_id}")
# async def edit_thesis_point(task_id: str, request: ThesisEditRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.edit_thesis_point(request.index, request.action, request.prompt)
#     return {"status": "success", **result}

# # ➕ Add Thesis Point
# # @router.post("/add-thesis-point/{task_id}")
# # async def add_thesis_point(task_id: str, request: AddThesisRequest):
# #     bot = bot_store.get(task_id)
# #     if not bot:
# #         raise HTTPException(status_code=404, detail="Bot not found")
# #     result = bot.add_thesis_point(request.prompt)
# #     return {"status": "success", **result}
# @router.post("/add-thesis-point/{task_id}")
# async def add_thesis_point(task_id: str, request: AddThesisRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.add_thesis_point(request.prompt)
#     if result["status"] == "error":
#         raise HTTPException(status_code=500, detail=result["error"])
#     return {
#         "status": "success",
#         "added_point": result["added_point"],
#         "elaborated_text": result["elaborated_text"],
#         "sources": result["sources"],
#         "pdf_base64": result["pdf_base64"]
#     }



# # 🔄 Adjust Length
# @router.post("/adjust-thesis-length/{task_id}")
# async def adjust_thesis_length(task_id: str, request: AdjustThesisRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.adjust_thesis_length(request.index, request.direction)
#     return {"status": "success", **result}



# # 🗑️ Clean Task State
# @router.delete("/clean/{task_id}")
# async def clean_task(task_id: str):
#     analyze_task_status.pop(task_id, None)
#     analyze_task_store.pop(task_id, None)
#     bot_store.pop(task_id, None)
#     return {"status": "cleared", "task_id": task_id}

# # 🔄 Unit Conversion
# @router.post("/convert-units/{task_id}")
# async def convert_units_route(task_id: str, request: UnitConversionRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.apply_unit_conversion(request.conversion_profile, request.custom_mappings)
#     return {"status": "success", **result}

# # 🔍 Elaborate Thesis Point
# @router.post("/elaborate-thesis-point/{task_id}")
# async def elaborate_thesis_point(task_id: str, request: ElaborateThesisPointRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     try:
#         elaborated_text = bot.elaborate_thesis_point(request.point_summary, request.word_count)
#         return {
#             "status": "success",
#             "elaborated_text": elaborated_text
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error elaborating thesis point: {str(e)}")


# # 💬 Chat Endpoint
# @router.post("/chat")
# async def chat(request: ChatRequest):
#     uploaded_files = session_store.get("uploaded_files", [])
#     if not all(f in [f[0] for f in uploaded_files] for f in request.files):
#         raise HTTPException(status_code=400, detail="One or more files not uploaded")
    
#     bot = FinanceBot(session_id=request.session_id)
#     try:
#         chat_history = json.loads(request.history)
#         # Rewind file objects to ensure they are readable
#         file_objects = [f[1] for f in uploaded_files if f[0] in request.files]
#         for obj in file_objects:
#             obj.seek(0)
#         response = bot.chat(request.files, request.query, chat_history, file_objects=file_objects)
#         chat_history.append({"role": "user", "content": request.query})
#         chat_history.append({"role": "assistant", "content": response})
#         bot.save_chat_history(chat_history)
#         return {
#             "response": response,
#             "history": json.dumps(chat_history)
#         }
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid history format")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")




#################################################################################################################################

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks,Query
from fastapi.responses import StreamingResponse,JSONResponse
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from io import BytesIO
import base64
import uuid
from f import FinanceBot
from rag_pipeline import convert_units, elaborate_on_thesis_point, format_sources_for_display, generate_styled_pdf,session_state
import os
import json
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")    

router = APIRouter()

# 📁 In-memory session-like storage
session_store = {
    "pdf_bytes": None,
    "company_name": "Report",
    "uploaded_files": None
}

# 🧰 In-memory stores
analyze_task_store = {}       # task_id -> result dict
analyze_task_status = {}      # task_id -> "pending" / "done" / "error"
bot_store = {}                # task_id -> FinanceBot instance

# 📦 Request Models
class ModifyRequest(BaseModel):
    section: str
    user_prompt: str

class UnitConversionRequest(BaseModel):
    conversion_profile: str
    custom_mappings: Optional[Dict[str, str]] = None

class ElaborateThesisPointRequest(BaseModel):
    point_summary: str
    word_count: int = 200

class ThesisEditRequest(BaseModel):
    index: int
    action: str  # 'delete', 'rewrite'
    prompt: Optional[str] = None

class AddThesisRequest(BaseModel):
    prompt: str
    # word_count: int = 150

class AdjustThesisRequest(BaseModel):
    index: int
    direction: str  # 'increase' or 'decrease'

class ChatRequest(BaseModel): 
    session_id: str = Field(..., description="Unique session identifier")
    files: List[str] = Field(..., description="List of filenames to chat with")
    query: str = Field(..., description="User's query or question")
    history: str = Field(default="[]", description="JSON string of chat history as list of {'role': 'user'|'assistant', 'content': str}")

# 🤔 Background Task
def analyze_background(task_id: str, file_tuples: List[tuple]):
    bot = FinanceBot(session_id=task_id)
    try:
        file_objs = [f[1] for f in file_tuples] 
        file_names = [f[0] for f in file_tuples]
        result = bot.analyze_documents(file_objs, file_names)

        analyze_task_store[task_id] = result
        analyze_task_status[task_id] = "done"
        bot_store[task_id] = bot

        session_store["pdf_bytes"] = result["pdf_bytes"]
        session_store["company_name"] = result["company_name"]
    except Exception as e:
        analyze_task_store[task_id] = {"status": "error", "errors": [str(e)]}
        analyze_task_status[task_id] = "error"

@router.post("/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        uploaded = []
        for file in files:
            content = await file.read()
            buffer = BytesIO(content)
            buffer.name = file.filename
            buffer.seek(0)
            uploaded.append((file.filename, buffer))

        # Safely get or initialize existing list
        existing = session_store.get("uploaded_files") or []
        existing_filenames = {f[0] for f in existing}
        new_files = [(name, buf) for name, buf in uploaded if name not in existing_filenames]

        existing.extend(new_files)
        session_store["uploaded_files"] = existing

        return {"status": "success", "filenames": [f[0] for f in session_store["uploaded_files"]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")



# 📄 Upload PDFs
# @router.post("/upload-files")
# async def upload_files(files: List[UploadFile] = File(...)):
#     try:
#         uploaded = []
#         for file in files:
#             content = await file.read()
#             buffer = BytesIO(content)
#             buffer.name = file.filename
#             uploaded.append((file.filename, buffer))
#         session_store["uploaded_files"] = uploaded
#         return {"status": "success", "filenames": [f[0] for f in uploaded]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


@router.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    try:
        uploaded_files = session_store.get("uploaded_files", [])
        for file_name, file_buffer in uploaded_files:
            if file_name == filename:
                file_buffer.seek(0)
                return StreamingResponse(
                    file_buffer,
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"inline; filename={filename}"}
                )
        raise HTTPException(status_code=404, detail=f"PDF {filename} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")

# 🤜 Trigger Analysis
@router.post("/analyze")
async def analyze_async(background_tasks: BackgroundTasks):
    try:
        if not session_store.get("uploaded_files"):
            raise HTTPException(status_code=400, detail="No files uploaded")

        task_id = str(uuid.uuid4())
        analyze_task_status[task_id] = "pending"
        background_tasks.add_task(analyze_background, task_id, session_store["uploaded_files"])

        return {"status": "processing", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting analysis: {str(e)}")

# 🔎 Check Status
@router.get("/status/{task_id}")
async def check_status(task_id: str):
    status = analyze_task_status.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return {"status": status}

# 📂 Get Result
@router.get("/result/{task_id}")
async def get_result(task_id: str):
    # result = analyze_task_store.get(task_id)
    bot=bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot.get_result()

# # 📄 PDF Download
# @router.get("/generate-pdf")
# async def generate_pdf():
#     try:
#         if not session_store["pdf_bytes"]:
#             raise HTTPException(status_code=400, detail="PDF not available.")
#         return StreamingResponse(
#             session_store["pdf_bytes"],
#             media_type="application/pdf",
#             headers={"Content-Disposition": f"inline; filename={session_store['company_name']}.pdf"}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")

# 📄 PDF Download
@router.get("/generate-pdf/{task_id}") 
async def generate_pdf(task_id: str):
    # Retrieve the specific bot instance for this task
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Analysis session not found.")

    # Check if the PDF object exists on the bot instance
    if not bot.pdf_generated_bytes:
        raise HTTPException(status_code=400, detail="PDF has not been generated for this session.")

    try:
        # Get the raw BytesIO object
        pdf_buffer = bot.pdf_generated_bytes
        # IMPORTANT: Rewind the buffer to the beginning before reading
        pdf_buffer.seek(0)

        company_name = bot.company_name or "report"

        # Stream the raw binary data
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={company_name}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")
# # 🖊️ Modify Report
# @router.post("/modify-report/{task_id}")
# async def modify_report(task_id: str, request: ModifyRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.modify_report(request.section, request.user_prompt)
#     if result["status"] == "error":
#         raise HTTPException(status_code=400, detail=result["errors"])
#     return {
#         "status": "success",
#         "section": request.section,
#         "modified_text": result["modified_section"],
#         "sources": result["sources"],
#         "pdf_base64": result["pdf_bytes"],
#         "key_thesis_points": result.get("key_thesis_points", []),
#         "detected_units": result["detected_units"]
#     }
@router.post("/modify-report/{task_id}")
async def modify_report(task_id: str, request: ModifyRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # ✅ Call modify_report (returns a dictionary, not a tuple!)
    result = bot.modify_report(request.section, request.user_prompt)

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("errors", ["Unknown error occurred."]))

    elif result.get("status") == "warning":
        return {
            "status": "warning",
            "message": result.get("errors", ["Modification issue occurred."]),
            "modified_text": result.get("modified_section", ""),
            "sources": [],
            "pdf_base64": None
        }

    return {
        "status": "success",
        "message": "Report section modified successfully.",
        "modified_text": result.get("modified_section", ""),
        "sources": result.get("sources", []),
        "pdf_base64": result.get("pdf_bytes", None),  
        "key_thesis_points": result.get("key_thesis_points", []),
        "detected_units": result.get("detected_units", {}),
        "errors": result.get("errors", [])
    }



# 💚 Edit Thesis
@router.post("/edit-thesis/{task_id}")
async def edit_thesis_point(task_id: str, request: ThesisEditRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    result = bot.edit_thesis_point(request.index, request.action, request.prompt)
    return {"status": "success", **result}

# ➕ Add Thesis Point
# @router.post("/add-thesis-point/{task_id}")
# async def add_thesis_point(task_id: str, request: AddThesisRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.add_thesis_point(request.prompt)
#     return {"status": "success", **result}
@router.post("/add-thesis-point/{task_id}")
async def add_thesis_point(task_id: str, request: AddThesisRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    result = bot.add_thesis_point(request.prompt)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    return {
        "status": "success",
        "added_point": result["added_point"],
        "elaborated_text": result["elaborated_text"],
        "sources": result["sources"],
        "pdf_base64": result["pdf_base64"]
    }



# 🔄 Adjust Length
@router.post("/adjust-thesis-length/{task_id}")
async def adjust_thesis_length(task_id: str, request: AdjustThesisRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    result = bot.adjust_thesis_length(request.index, request.direction)
    return {"status": "success", **result}



# 🗑️ Clean Task State
@router.delete("/clean/{task_id}")
async def clean_task(task_id: str):
    analyze_task_status.pop(task_id, None)
    analyze_task_store.pop(task_id, None)
    bot_store.pop(task_id, None)
    return {"status": "cleared", "task_id": task_id}

# 🔄 Unit Conversion
@router.post("/convert-units/{task_id}")
async def convert_units_route(task_id: str, request: UnitConversionRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    result = bot.apply_unit_conversion(request.conversion_profile, request.custom_mappings)
    return {"status": "success", **result}

# 🔍 Elaborate Thesis Point
@router.post("/elaborate-thesis-point/{task_id}")
async def elaborate_thesis_point(task_id: str, request: ElaborateThesisPointRequest):
    bot = bot_store.get(task_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    try:
        elaborated_text = bot.elaborate_thesis_point(request.point_summary, request.word_count)
        return {
            "status": "success",
            "elaborated_text": elaborated_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error elaborating thesis point: {str(e)}")


# 💬 Chat Endpoint
@router.post("/chat")
async def chat(request: ChatRequest):
    uploaded_files = session_store.get("uploaded_files", [])
    if not all(f in [f[0] for f in uploaded_files] for f in request.files):
        raise HTTPException(status_code=400, detail="One or more files not uploaded")

    bot = FinanceBot(session_id=request.session_id)
    try:
        chat_history = json.loads(request.history)
        file_objects = [f[1] for f in uploaded_files if f[0] in request.files]
        for obj in file_objects:
            obj.seek(0)

        # Get raw HTML response string
        response = bot.chat(request.files, request.query, chat_history, file_objects=file_objects)
        chat_history.append({"role": "user", "content": request.query})
        chat_history.append({"role": "assistant", "content": response})
        bot.save_chat_history(chat_history)
        return {
             "response": response,
             "history": json.dumps(chat_history)
         }
        #return response  # ✅ Return raw string (not a JSON object)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.get("/citation-text")
async def get_full_pdf_with_highlight(
    filename: str = Query(...),
    page: int = Query(...),
    highlight: Optional[str] = Query(None)
):
    try:
        full_text_map = session_state.full_pdf_text_map
        all_pages = full_text_map.get(filename)

        if not all_pages:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "File not found"}
            )

        highlighted_pages = {}
        for pg_num, text in all_pages.items():
            if pg_num == page and highlight and highlight in text:
                text = text.replace(highlight, f"<mark>{highlight}</mark>")
            highlighted_pages[pg_num] = text

        return {
            "status": "success",
            "filename": filename,
            "highlighted_page": page,
            "pages": highlighted_pages  # dict of {page_num: text}
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)})

# # @router.get("/citation-text")
# # async def get_citation_text(
# #     filename: str = Query(...),
# #     page: int = Query(...),
# #     highlight: Optional[str] = Query(None)
# # ):
# #     try:
# #         full_text_map = session_state.full_pdf_text_map
# #         page_text = full_text_map.get(filename, {}).get(page)

# #         if not page_text:
# #             return JSONResponse(
# #                 status_code=404,
# #                 content={"status": "error", "message": "Text not found for given file and page."}
# #             )

# #         # Simple highlight: wrap matched context in <mark>
# #         if highlight and highlight in page_text:
# #             highlighted_text = page_text.replace(highlight, f"<mark>{highlight}</mark>")
# #         else:
# #             highlighted_text = page_text

# #         return {
# #             "status": "success",
# #             "filename": filename,
# #             "page": page,
# #             "text": highlighted_text
# #         }

# #     except Exception as e:
# #         return JSONResponse(
# #             status_code=500,
# #             content={"status": "error", "message": str(e)}
# #         )



#########################################################################################################################################


# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks,Query
# from fastapi.responses import StreamingResponse,JSONResponse
# from typing import List, Dict, Optional
# from pydantic import BaseModel, Field
# from io import BytesIO
# import base64
# import uuid
# from f import FinanceBot
# from rag_pipeline import convert_units, elaborate_on_thesis_point, format_sources_for_display, generate_styled_pdf,session_state
# import os
# import json
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")    

# router = APIRouter()

# # 📁 In-memory session-like storage
# session_store = {
#     "pdf_bytes": None,
#     "company_name": "Report",
#     "uploaded_files": None
# }

# # 🧰 In-memory stores
# analyze_task_store = {}       # task_id -> result dict
# analyze_task_status = {}      # task_id -> "pending" / "done" / "error"
# bot_store = {}                # task_id -> FinanceBot instance

# # 📦 Request Models
# class ModifyRequest(BaseModel):
#     section: str
#     user_prompt: str

# class UnitConversionRequest(BaseModel):
#     conversion_profile: str
#     custom_mappings: Optional[Dict[str, str]] = None

# class ElaborateThesisPointRequest(BaseModel):
#     point_summary: str
#     word_count: int = 200

# class ThesisEditRequest(BaseModel):
#     index: int
#     action: str  # 'delete', 'rewrite'
#     prompt: Optional[str] = None

# class AddThesisRequest(BaseModel):
#     prompt: str
#     # word_count: int = 150

# class AdjustThesisRequest(BaseModel):
#     index: int
#     direction: str  # 'increase' or 'decrease'

# class ChatRequest(BaseModel): 
#     session_id: str = Field(..., description="Unique session identifier")
#     files: List[str] = Field(..., description="List of filenames to chat with")
#     query: str = Field(..., description="User's query or question")
#     history: str = Field(default="[]", description="JSON string of chat history as list of {'role': 'user'|'assistant', 'content': str}")

# # 🤔 Background Task
# def analyze_background(task_id: str, file_tuples: List[tuple]):
#     bot = FinanceBot(session_id=task_id)
#     try:
#         file_objs = [f[1] for f in file_tuples] 
#         file_names = [f[0] for f in file_tuples]
#         result = bot.analyze_documents(file_objs, file_names)

#         analyze_task_store[task_id] = result
#         analyze_task_status[task_id] = "done"
#         bot_store[task_id] = bot

#         session_store["pdf_bytes"] = result["pdf_bytes"]
#         session_store["company_name"] = result["company_name"]
#     except Exception as e:
#         analyze_task_store[task_id] = {"status": "error", "errors": [str(e)]}
#         analyze_task_status[task_id] = "error"

# @router.post("/upload-files")
# async def upload_files(files: List[UploadFile] = File(...)):
#     try:
#         uploaded = []
#         for file in files:
#             content = await file.read()
#             buffer = BytesIO(content)
#             buffer.name = file.filename
#             buffer.seek(0)
#             uploaded.append((file.filename, buffer))

#         # Safely get or initialize existing list
#         existing = session_store.get("uploaded_files") or []
#         existing_filenames = {f[0] for f in existing}
#         new_files = [(name, buf) for name, buf in uploaded if name not in existing_filenames]

#         existing.extend(new_files)
#         session_store["uploaded_files"] = existing

#         return {"status": "success", "filenames": [f[0] for f in session_store["uploaded_files"]]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")



# # 📄 Upload PDFs
# # @router.post("/upload-files")
# # async def upload_files(files: List[UploadFile] = File(...)):
# #     try:
# #         uploaded = []
# #         for file in files:
# #             content = await file.read()
# #             buffer = BytesIO(content)
# #             buffer.name = file.filename
# #             uploaded.append((file.filename, buffer))
# #         session_store["uploaded_files"] = uploaded
# #         return {"status": "success", "filenames": [f[0] for f in uploaded]}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


# @router.get("/get-pdf/{filename}")
# async def get_pdf(filename: str):
#     try:
#         uploaded_files = session_store.get("uploaded_files", [])
#         for file_name, file_buffer in uploaded_files:
#             if file_name == filename:
#                 file_buffer.seek(0)
#                 return StreamingResponse(
#                     file_buffer,
#                     media_type="application/pdf",
#                     headers={"Content-Disposition": f"inline; filename={filename}"}
#                 )
#         raise HTTPException(status_code=404, detail=f"PDF {filename} not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")

# # 📄 Extract and return full PDF text (all pages)
# # from fastapi import HTTPException
# import fitz  # PyMuPDF

# @router.get("/full-pdf-text/{filename}")
# async def get_full_pdf_text(filename: str):
#     """
#     Returns the extracted text for each page of the given PDF file.
#     """
#     uploaded_files = session_store.get("uploaded_files", [])
#     for file_name, file_buffer in uploaded_files:
#         if file_name == filename:
#             try:
#                 file_buffer.seek(0)
#                 doc = fitz.open(stream=file_buffer.read(), filetype="pdf")
#                 pages_text = [doc[i].get_text("text") for i in range(len(doc))]
#                 return {
#                     "status": "success",
#                     "pages": pages_text
#                 }
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

#     raise HTTPException(status_code=404, detail="File not found")


# # 🤜 Trigger Analysis
# @router.post("/analyze")
# async def analyze_async(background_tasks: BackgroundTasks):
#     try:
#         if not session_store.get("uploaded_files"):
#             raise HTTPException(status_code=400, detail="No files uploaded")

#         task_id = str(uuid.uuid4())
#         analyze_task_status[task_id] = "pending"
#         background_tasks.add_task(analyze_background, task_id, session_store["uploaded_files"])

#         return {"status": "processing", "task_id": task_id}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error starting analysis: {str(e)}")

# # 🔎 Check Status
# @router.get("/status/{task_id}")
# async def check_status(task_id: str):
#     status = analyze_task_status.get(task_id)
#     if not status:
#         raise HTTPException(status_code=404, detail="Task ID not found")
#     return {"status": status}

# # 📂 Get Result
# @router.get("/result/{task_id}")
# async def get_result(task_id: str):
#     # result = analyze_task_store.get(task_id)
#     bot=bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     return bot.get_result()

# # # 📄 PDF Download
# # @router.get("/generate-pdf")
# # async def generate_pdf():
# #     try:
# #         if not session_store["pdf_bytes"]:
# #             raise HTTPException(status_code=400, detail="PDF not available.")
# #         return StreamingResponse(
# #             session_store["pdf_bytes"],
# #             media_type="application/pdf",
# #             headers={"Content-Disposition": f"inline; filename={session_store['company_name']}.pdf"}
# #         )
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")

# # 📄 PDF Download
# @router.get("/generate-pdf/{task_id}") 
# async def generate_pdf(task_id: str):
#     # Retrieve the specific bot instance for this task
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Analysis session not found.")

#     # Check if the PDF object exists on the bot instance
#     if not bot.pdf_generated_bytes:
#         raise HTTPException(status_code=400, detail="PDF has not been generated for this session.")

#     try:
#         # Get the raw BytesIO object
#         pdf_buffer = bot.pdf_generated_bytes
#         # IMPORTANT: Rewind the buffer to the beginning before reading
#         pdf_buffer.seek(0)

#         company_name = bot.company_name or "report"

#         # Stream the raw binary data
#         return StreamingResponse(
#             pdf_buffer,
#             media_type="application/pdf",
#             headers={"Content-Disposition": f"inline; filename={company_name}.pdf"}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error streaming PDF: {str(e)}")
# # # 🖊️ Modify Report
# # @router.post("/modify-report/{task_id}")
# # async def modify_report(task_id: str, request: ModifyRequest):
# #     bot = bot_store.get(task_id)
# #     if not bot:
# #         raise HTTPException(status_code=404, detail="Bot not found")
# #     result = bot.modify_report(request.section, request.user_prompt)
# #     if result["status"] == "error":
# #         raise HTTPException(status_code=400, detail=result["errors"])
# #     return {
# #         "status": "success",
# #         "section": request.section,
# #         "modified_text": result["modified_section"],
# #         "sources": result["sources"],
# #         "pdf_base64": result["pdf_bytes"],
# #         "key_thesis_points": result.get("key_thesis_points", []),
# #         "detected_units": result["detected_units"]
# #     }
# @router.post("/modify-report/{task_id}")
# async def modify_report(task_id: str, request: ModifyRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")

#     # ✅ Call modify_report (returns a dictionary, not a tuple!)
#     result = bot.modify_report(request.section, request.user_prompt)

#     if result.get("status") == "error":
#         raise HTTPException(status_code=400, detail=result.get("errors", ["Unknown error occurred."]))

#     elif result.get("status") == "warning":
#         return {
#             "status": "warning",
#             "message": result.get("errors", ["Modification issue occurred."]),
#             "modified_text": result.get("modified_section", ""),
#             "sources": [],
#             "pdf_base64": None
#         }

#     return {
#         "status": "success",
#         "message": "Report section modified successfully.",
#         "modified_text": result.get("modified_section", ""),
#         "sources": result.get("sources", []),
#         "pdf_base64": result.get("pdf_bytes", None),  
#         "key_thesis_points": result.get("key_thesis_points", []),
#         "detected_units": result.get("detected_units", {}),
#         "errors": result.get("errors", [])
#     }



# # 💚 Edit Thesis
# @router.post("/edit-thesis/{task_id}")
# async def edit_thesis_point(task_id: str, request: ThesisEditRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.edit_thesis_point(request.index, request.action, request.prompt)
#     return {"status": "success", **result}

# # ➕ Add Thesis Point
# # @router.post("/add-thesis-point/{task_id}")
# # async def add_thesis_point(task_id: str, request: AddThesisRequest):
# #     bot = bot_store.get(task_id)
# #     if not bot:
# #         raise HTTPException(status_code=404, detail="Bot not found")
# #     result = bot.add_thesis_point(request.prompt)
# #     return {"status": "success", **result}
# @router.post("/add-thesis-point/{task_id}")
# async def add_thesis_point(task_id: str, request: AddThesisRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.add_thesis_point(request.prompt)
#     if result["status"] == "error":
#         raise HTTPException(status_code=500, detail=result["error"])
#     return {
#         "status": "success",
#         "added_point": result["added_point"],
#         "elaborated_text": result["elaborated_text"],
#         "sources": result["sources"],
#         "pdf_base64": result["pdf_base64"]
#     }



# # 🔄 Adjust Length
# @router.post("/adjust-thesis-length/{task_id}")
# async def adjust_thesis_length(task_id: str, request: AdjustThesisRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.adjust_thesis_length(request.index, request.direction)
#     return {"status": "success", **result}



# # 🗑️ Clean Task State
# @router.delete("/clean/{task_id}")
# async def clean_task(task_id: str):
#     analyze_task_status.pop(task_id, None)
#     analyze_task_store.pop(task_id, None)
#     bot_store.pop(task_id, None)
#     return {"status": "cleared", "task_id": task_id}

# # 🔄 Unit Conversion
# @router.post("/convert-units/{task_id}")
# async def convert_units_route(task_id: str, request: UnitConversionRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     result = bot.apply_unit_conversion(request.conversion_profile, request.custom_mappings)
#     return {"status": "success", **result}

# # 🔍 Elaborate Thesis Point
# @router.post("/elaborate-thesis-point/{task_id}")
# async def elaborate_thesis_point(task_id: str, request: ElaborateThesisPointRequest):
#     bot = bot_store.get(task_id)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     try:
#         elaborated_text = bot.elaborate_thesis_point(request.point_summary, request.word_count)
#         return {
#             "status": "success",
#             "elaborated_text": elaborated_text
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error elaborating thesis point: {str(e)}")


# # 💬 Chat Endpoint
# @router.post("/chat")
# async def chat(request: ChatRequest):
#     uploaded_files = session_store.get("uploaded_files", [])
#     if not all(f in [f[0] for f in uploaded_files] for f in request.files):
#         raise HTTPException(status_code=400, detail="One or more files not uploaded")

#     bot = FinanceBot(session_id=request.session_id)
#     try:
#         chat_history = json.loads(request.history)
#         file_objects = [f[1] for f in uploaded_files if f[0] in request.files]
#         for obj in file_objects:
#             obj.seek(0)

#         # Get raw HTML response string
#         response = bot.chat(request.files, request.query, chat_history, file_objects=file_objects)
#         chat_history.append({"role": "user", "content": request.query})
#         chat_history.append({"role": "assistant", "content": response})
#         bot.save_chat_history(chat_history)
#         return {
#              "response": response,
#              "history": json.dumps(chat_history)
#          }
#         #return response  # ✅ Return raw string (not a JSON object)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid history format")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

# @router.get("/citation-text")
# async def get_full_pdf_with_highlight(
#     filename: str = Query(...),
#     page: int = Query(...),
#     highlight: Optional[str] = Query(None)
# ):
#     try:
#         full_text_map = session_state.full_pdf_text_map
#         all_pages = full_text_map.get(filename)

#         if not all_pages:
#             return JSONResponse(
#                 status_code=404,
#                 content={"status": "error", "message": "File not found"}
#             )

#         highlighted_pages = {}
#         for pg_num, text in all_pages.items():
#             if pg_num == page and highlight and highlight in text:
#                 text = text.replace(highlight, f"<mark>{highlight}</mark>")
#             highlighted_pages[pg_num] = text

#         return {
#             "status": "success",
#             "filename": filename,
#             "highlighted_page": page,
#             "pages": highlighted_pages  # dict of {page_num: text}
#         }

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"status": "error", "message": str(e)})

# # # @router.get("/citation-text")
# # # async def get_citation_text(
# # #     filename: str = Query(...),
# # #     page: int = Query(...),
# # #     highlight: Optional[str] = Query(None)
# # # ):
# # #     try:
# # #         full_text_map = session_state.full_pdf_text_map
# # #         page_text = full_text_map.get(filename, {}).get(page)

# # #         if not page_text:
# # #             return JSONResponse(
# # #                 status_code=404,
# # #                 content={"status": "error", "message": "Text not found for given file and page."}
# # #             )

# # #         # Simple highlight: wrap matched context in <mark>
# # #         if highlight and highlight in page_text:
# # #             highlighted_text = page_text.replace(highlight, f"<mark>{highlight}</mark>")
# # #         else:
# # #             highlighted_text = page_text

# # #         return {
# # #             "status": "success",
# # #             "filename": filename,
# # #             "page": page,
# # #             "text": highlighted_text
# # #         }

# # #     except Exception as e:
# # #         return JSONResponse(
# # #             status_code=500,
# # #             content={"status": "error", "message": str(e)}
# # #         )

