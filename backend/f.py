# import os
# import io
# import base64
# import hashlib
# import re 
# import time
# from typing import List, Dict, Tuple, Set, Optional
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.retrievers import MultiQueryRetriever
# from langchain_core.runnables import RunnablePassthrough, RunnableParallel
# from operator import itemgetter
# import torch
# from sentence_transformers import SentenceTransformer
# from langchain_core.prompts import PromptTemplate
# from rag_pipeline import (
#     clean_company_name, extract_text_from_pdfs, create_faiss_vectorstore, get_company_name_from_llm,
#     extract_company_name_fallback_regex, generate_styled_pdf, modify_report_section,
#     validate_and_rerun_quarterly_earnings, extract_key_thesis_points, elaborate_on_thesis_point,
#     format_sources_for_display, convert_units,add_inline_citations
# )

# from prompt_templates import (
#     get_business_overview_prompt_template, get_quarterly_earnings_prompt_template,
#     get_investment_thesis_prompt_template
# )
 
# # Set torch path to avoid issues 
# torch.classes.__path__ = []

# import nltk
# nltk.download('punkt', quiet=True)

# # --- Global Variables & Constants ---
# DEFAULT_COMPANY_NAME = "Company Analysis Report"
# sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# class FinanceBot:
#     def load_chat_history(self):
#         if not self.session_id:
#             return []
#         return self.session_data.get(f"chat_history_{self.session_id}", [])

#     def save_chat_history(self, history):
#         if self.session_id:
#             self.session_data[f"chat_history_{self.session_id}"] = history

#     def __init__(self, session_id=None):
#         self.session_id = session_id
#         self.session_data = {}
#         self.chat_history = self.load_chat_history() if session_id else []
#         self.company_name = DEFAULT_COMPANY_NAME
#         self.vectordb = None
#         self.num_docs = 0
#         self.raw_text = ""
#         self.llm_business_overview = ""
#         self.llm_quarterly_highlights = ""
#         self.llm_investment_thesis = ""
#         self.business_overview_sources = []
#         self.quarterly_highlights_sources = []
#         self.investment_thesis_sources = []
#         self.global_references: Set[str] = set()
#         self.global_citation_details_map: Dict[str, str] = {}
#         self.global_citation_details_list: List[Dict] = []
#         self.key_thesis_points = []
#         self.current_thesis_paragraphs = []
#         self.pdf_generated_bytes: Optional[io.BytesIO] = None
#         self.detected_units = {}
#         self.custom_unit_mappings = {
#             "%": "percentage", "~": "approximately", "$": "US dollar", "(Y/Y)": "year-on-year",
#             "€": "Euro", "million": "M", "<": "less than", ">": "greater than",
#             "Euro": "€", "USD": "$"
#         }
#         self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
#                                 google_api_key=os.getenv("GOOGLE_API_KEY"),
#                             temperature=0.0)

#     def chat(self, files: List[str], query: str, history: List[Dict[str, str]], file_objects: Optional[List[io.BytesIO]] = None) -> Tuple[str, List[str]]:
#         """
#         Process a user query using the RAG pipeline and return a response with sources.
        
#         Args:
#             files (List[str]): List of filenames to use for context.
#             query (str): User's query or question.
#             history (List[Dict[str, str]]): Chat history containing user and assistant messages.
#             file_objects (Optional[List[io.BytesIO]]): List of file objects corresponding to filenames, if available.
        
#         Returns:
#             Tuple[str, List[str]]: The generated response and a list of formatted source references.
#         """
#         if not self.vectordb:
#             if not files or not file_objects:
#                 return "No context available to answer the query. Please upload relevant files.", []
            
#             if len(file_objects) != len(files):
#                 return "Mismatch between filenames and file objects.", []
            
#             # Extract text from file objects with proper tuple handling
#             all_docs, raw_text, _, error = extract_text_from_pdfs(file_objects)
#             if error or not all_docs:
#                 return f"Error extracting text from files: {error or 'No text extracted'}", []
            
#             self.raw_text = raw_text
#             self.num_docs = len(all_docs)
            
#             # Create vector store with error handling
#             self.vectordb, _, error = create_faiss_vectorstore(all_docs)
#             if error or self.vectordb is None:
#                 return f"Error creating vector store: {error or 'Vector store creation failed'}", []

#         # Define a prompt template for the chat query
#         chat_prompt_template = PromptTemplate.from_template(
#             """
#             You are a financial analyst assistant. Use the provided context to answer the user's query accurately and concisely.
#             Incorporate relevant information from the chat history if applicable.
#             If specific details are not available in the context, clearly state so and provide a general response if possible.
            
#             Chat History:
#             {history}
            
#             Context:
#             {context}
            
#             Query:
#             {query}
            
#             Answer:
#             """
#         )

#         # Format chat history for the prompt
#         formatted_history = ""
#         for msg in history:
#             role = msg.get("role", "").capitalize()
#             content = msg.get("content", "")
#             formatted_history += f"{role}: {content}\n"
        
#         # Set up the retriever
#         try:
#             retriever = MultiQueryRetriever.from_llm( 
#                 retriever=self.vectordb.as_retriever(search_kwargs={"k": 10}),
#                 llm=self.llm
#             )
#         except Exception as e:
#             return f"Error initializing retriever: {str(e)}", []

#         # Create the document chain
#         doc_chain = create_stuff_documents_chain(self.llm, chat_prompt_template)

#         # Set up the RAG chain
#         rag_chain = (
#             {
#                 "context": retriever,
#                 "query": RunnablePassthrough(),
#                 "history": lambda x: formatted_history
#             }
#             | doc_chain
#         )

#         # Execute the query
#         try:
#             response = rag_chain.invoke(query)
#             retrieved_docs = retriever.invoke(query) 
#             #sources = format_sources_for_display(retrieved_docs, self.global_references, self.global_citation_details_map)
#             #ources = format_sources_for_display(retrieved_docs)
#             # response, detected_units = convert_units(response, self.custom_unit_mappings)
#             # self.detected_units.update(detected_units)
            
#             response = add_inline_citations(response, retrieved_docs)
#             return response 
#         except Exception as e:
#             return f"Error processing query: {str(e)}", []

#     def analyze_documents(self, uploaded_files: List[io.BytesIO], file_names: List[str]) -> Dict:
#         """
#         Analyze uploaded PDF documents and generate insights.
#         """
#         result = {
#             "status": "success",
#             "company_name": self.company_name,
#             "business_overview": "",
#             "quarterly_highlights": "",
#             "investment_thesis": "",
#             "key_thesis_points": [],
#             "pdf_bytes": None,
#             "references": [],
#             "errors": []
#         }

#         # Reset internal state
#         self.vectordb = None
#         self.num_docs = 0
#         self.raw_text = ""
#         self.llm_business_overview = ""
#         self.llm_quarterly_highlights = ""
#         self.llm_investment_thesis = ""
#         self.business_overview_sources = []
#         self.quarterly_highlights_sources = []
#         self.investment_thesis_sources = []
#         self.global_references = set()
#         self.global_citation_details_map = {}
#         self.global_citation_details_list = []
#         self.key_thesis_points = []
#         self.current_thesis_paragraphs = []

#         if not uploaded_files:
#             result.update({
#                 "status": "error",
#                 "errors": ["No files uploaded. Please provide PDF documents."],
#                 "business_overview": "No text extracted from PDFs.",
#                 "quarterly_highlights": "No text extracted from PDFs.",
#                 "investment_thesis": "No text extracted from PDFs."
#             })
#             return result

#         # Extract text from PDFs
#         all_docs, raw_text, _, error = extract_text_from_pdfs(uploaded_files)
#         self.raw_text = raw_text

#         if error or not all_docs:
#             result.update({
#                 "status": "error",
#                 "errors": [error or "Could not extract any text from the uploaded PDF files."],
#                 "business_overview": "No text extracted from PDFs.",
#                 "quarterly_highlights": "No text extracted from PDFs.",
#                 "investment_thesis": "No text extracted from PDFs."
#             })
#             return result

#         # Create vector store
#         self.vectordb, self.num_docs, error = create_faiss_vectorstore(all_docs)
#         if error:
#             result.update({
#                 "status": "error",
#                 "errors": [error],
#                 "business_overview": "Vector store error prevented analysis.",
#                 "quarterly_highlights": "Vector store error prevented analysis.",
#                 "investment_thesis": "Vector store error prevented analysis."
#             })
#             return result

#         # Initialize LLM
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=GOOGLE_API_KEY,
#             temperature=0.0,
#         )

#         # Extract company name
#         self.company_name = get_company_name_from_llm(llm, self.raw_text, file_names)
#         if self.company_name == DEFAULT_COMPANY_NAME:
#             self.company_name = extract_company_name_fallback_regex(self.raw_text, file_names)
#         result["company_name"] = self.company_name

#         # Generate Business Overview
#         try:
#             k_value = min(70, self.num_docs) if self.num_docs > 0 else 1
#             retriever = MultiQueryRetriever.from_llm(
#                 retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
#             )
#             chain = create_stuff_documents_chain(llm, get_business_overview_prompt_template())
#             rag = (
#                 RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
#                 | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
#             )
#             time.sleep(3)
#             response = rag.invoke({
#                 "input": f"Generate a detailed business overview of {self.company_name} based on its core business, revenue segments (with percentages) and what each segment encompasses, geographic distribution (with percentages), headquarters, stock exchange with its names, and employee count."
#             })
#             self.llm_business_overview = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))
#             self.business_overview_sources = response.get("source_documents", [])
#             result["business_overview"] = self.llm_business_overview
#             if not self.llm_business_overview or len(self.llm_business_overview) < 50 or \
#                any(keyword in self.llm_business_overview.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
#                 result["errors"].append("Business Overview: Insufficient data detected.")
#         except Exception as e:
#             result["errors"].append(f"Error generating Business Overview: {str(e)}")
#             self.llm_business_overview = "Error generating business overview."
#             result["business_overview"] = self.llm_business_overview

#         # Generate Quarterly Earnings
#         try:
#             k_value = min(50, self.num_docs) if self.num_docs > 0 else 1
#             retriever = MultiQueryRetriever.from_llm(
#                 retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
#             )
#             chain = create_stuff_documents_chain(llm, get_quarterly_earnings_prompt_template())
#             rag = (
#                 RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
#                 | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
#             )
#             time.sleep(3)
#             response = rag.invoke({
#                 "input": f"For {self.company_name}, compare the financial performance of Q1 2025 with Q1 2024, including revenue, EBIT, adjusted EBIT, margin with y/y changes, and full-year 2025 outlook."
#             })
#             self.llm_quarterly_highlights = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))      
#             initial_quarterly_highlights = response["answer"].strip()
#             self.quarterly_highlights_sources = response.get("source_documents", [])
#             annotated_text, sources, error = validate_and_rerun_quarterly_earnings(
#                 self.vectordb, self.company_name, initial_quarterly_highlights, self.num_docs
#             )
#             self.llm_quarterly_highlights = annotated_text
#             if sources:
#                 self.quarterly_highlights_sources = sources
#             result["quarterly_highlights"] = self.llm_quarterly_highlights
#             if error:
#                 result["errors"].append(error)
#         except Exception as e:
#             result["errors"].append(f"Error generating Quarterly Highlights: {str(e)}")
#             self.llm_quarterly_highlights = "Error generating quarterly highlights."
#             result["quarterly_highlights"] = self.llm_quarterly_highlights

#         # Generate Investment Thesis
#         try:
#             k_value = min(50, self.num_docs) if self.num_docs > 0 else 1
#             retriever = MultiQueryRetriever.from_llm(
#                 retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
#             )
#             chain = create_stuff_documents_chain(llm, get_investment_thesis_prompt_template())
#             rag = (
#                 RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
#                 | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
#             )
#             time.sleep(3)
#             response = rag.invoke({
#                 "input": f"Construct a detailed investment thesis for {self.company_name}."
#             })
#             self.llm_investment_thesis = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))
#             self.investment_thesis_sources = response.get("source_documents", [])
#             self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]
#             result["investment_thesis"] = self.llm_investment_thesis
#             if not self.llm_investment_thesis or len(self.llm_investment_thesis) < 50 or \
#                any(keyword in self.llm_investment_thesis.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
#                 result["errors"].append("Investment Thesis: Insufficient data detected.")
#         except Exception as e:
#             result["errors"].append(f"Error generating Investment Thesis: {str(e)}")
#             self.llm_investment_thesis = "Error generating investment thesis."
#             result["investment_thesis"] = self.llm_investment_thesis

#         # Extract Key Thesis Points
#         try:
#             self.key_thesis_points, error = extract_key_thesis_points(vectordb=self.vectordb, num_docs=self.num_docs)
#             result["key_thesis_points"] = self.key_thesis_points
#             if error:
#                 result["errors"].append(error)
#         except Exception as e:
#             result["errors"].append(f"Error extracting key thesis points: {str(e)}")

#         # Generate PDF
#         try:
#             self.pdf_generated_bytes, error =  generate_styled_pdf(
#                 self.company_name,
#                 self.llm_business_overview or "",
#                 self.llm_quarterly_highlights or "", 
#                 self.llm_investment_thesis or "",
                
#             )
#             #result["pdf_bytes"] = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None
#             result["pdf_bytes"] = self.pdf_generated_bytes
#             if error:
#                 result["errors"].append(error)
#         except Exception as e:
#             result["errors"].append(f"Error generating PDF: {str(e)}")

#         # Detect units 
#         combined_text = f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}"
#         # self.detected_units = detect_units_in_text(combined_text)
#         # result["detected_units"] = self.detected_units

#         return result

#     def apply_unit_conversion(self, conversion_profile: str, custom_mappings: Optional[Dict[str, str]] = None) -> Dict:
#         result = {
#             "status": "success",
#             "business_overview": "",
#             "quarterly_highlights": "",
#             "investment_thesis": "",
#             "pdf_bytes": None,
#             "errors": []
#         }

#         custom_mappings = custom_mappings or self.custom_unit_mappings
#         try:
#             if self.llm_business_overview:
#                 self.llm_business_overview = convert_units(self.llm_business_overview, conversion_profile, custom_mappings)
#             if self.llm_quarterly_highlights:
#                 self.llm_quarterly_highlights = convert_units(self.llm_quarterly_highlights, conversion_profile, custom_mappings)
#             if self.llm_investment_thesis:
#                 self.llm_investment_thesis = convert_units(self.llm_investment_thesis, conversion_profile, custom_mappings)
#                 self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]

#             self.pdf_generated_bytes, error = generate_styled_pdf(
#                 self.company_name,
#                 self.llm_business_overview or "",
#                 self.llm_quarterly_highlights or "",
#                 self.llm_investment_thesis or "",
                
#             )
#             result.update({
#                 "business_overview": self.llm_business_overview,
#                 "quarterly_highlights": self.llm_quarterly_highlights,
#                 "investment_thesis": self.llm_investment_thesis,
#                 "pdf_bytes": base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None,
#                 "detected_units": detect_units_in_text(f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}")
#             })
#             if error:
#                 result["errors"].append(error)
#         except Exception as e:
#             result.update({
#                 "status": "error",
#                 "errors": [f"Error applying unit conversion: {str(e)}"]
#             })

#         return result

#     def modify_report(self, section: str, modification_prompt: str) -> Dict:
#         result = {
#             "status": "success",
#             "modified_section": "",
#             "section_name": section,
#             "sources": [],
#             "pdf_bytes": None,
#             "errors": []
#         }

#         if not modification_prompt:
#             result.update({"status": "error", "errors": ["Modification prompt is required."]})
#             return result

#         current_content = ""
#         if section.lower() in ["business overview", "overview"]:
#             current_content = self.llm_business_overview
#         elif section.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
#             current_content = self.llm_quarterly_highlights
#         elif section.lower() in ["investment thesis", "thesis"]:
#             current_content = self.llm_investment_thesis
#         else:
#             result.update({"status": "error", "errors": [f"Invalid section: {section}"]})
#             return result

#         try:
#             modified_text_annotated, sources, error = modify_report_section(
#                 self.vectordb,
#                 modification_prompt,
#                 section,
#                 self.company_name,
#                 self.num_docs,
#                 current_content
#             )
#             if modified_text_annotated:
#                 if section.lower() in ["business overview", "overview"]:
#                     self.llm_business_overview = modified_text_annotated
#                     self.business_overview_sources = sources
#                     result["modified_section"] = self.llm_business_overview
#                 elif section.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
#                     self.llm_quarterly_highlights = modified_text_annotated
#                     self.quarterly_highlights_sources = sources
#                     result["modified_section"] = self.llm_quarterly_highlights
#                 elif section.lower() in ["investment thesis", "thesis"]:
#                     self.llm_investment_thesis = modified_text_annotated
#                     self.investment_thesis_sources = sources
#                     self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]
#                     self.key_thesis_points, error = extract_key_thesis_points(self.vectordb, self.num_docs)
#                     result["modified_section"] = self.llm_investment_thesis
#                     result["key_thesis_points"] = self.key_thesis_points
#                     if error:
#                         result["errors"].append(error)

#                 self.pdf_generated_bytes, error = generate_styled_pdf(
#                     self.company_name,
#                     self.llm_business_overview or "",
#                     self.llm_quarterly_highlights or "",
#                     self.llm_investment_thesis or "",
                    
#                 )
#                 result["pdf_bytes"] = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None
#                 result["sources"] = format_sources_for_display(sources)
#                 result["detected_units"] = detect_units_in_text(f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}")
#                 if error:
#                     result["errors"].append(error)
#             else:
#                 result.update({"status": "error", "errors": ["Failed to modify the section."]})
#         except Exception as e:
#             result.update({"status": "error", "errors": [f"Error modifying {section}: {str(e)}"]})

#         return result
#     def edit_thesis_point(self, index: int, action: str, prompt: Optional[str] = None) -> Dict:
#         if not (0 <= index < len(self.current_thesis_paragraphs)):
#             return {"status": "error", "message": "Invalid index for thesis paragraph."}
        
#         if action == "delete":
#             self.current_thesis_paragraphs.pop(index)
#         elif action == "rewrite":
#             if not prompt:
#                 return {"status": "error", "message": "Rewrite requires a prompt."}
#             self.current_thesis_paragraphs[index] = prompt
#         else:
#             return {"status": "error", "message": f"Unsupported action: {action}"}

#         self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)
#         return {
#             "updated_thesis": self.llm_investment_thesis,
#             "key_thesis_points": self.key_thesis_points
#         }

  
#     # def add_thesis_point(self, prompt: str) -> Dict:
    
#     #     try:
#     #         # Save the key thesis point
#     #         self.key_thesis_points.append(prompt)

#     #         # Elaborate the point using default 200 words
#     #         elaborated, error = elaborate_on_thesis_point(
#     #             point=prompt,
#     #             word_count=200,
#     #             vectordb=self.vectordb,
#     #             num_docs=self.num_docs
#     #         )

#     #         if error:
#     #             return {
#     #                 "added_point": prompt,
#     #                 "elaborated_text": "",
#     #                 "error": error
#     #             }

#     #         # Append to thesis paragraphs
#     #         self.current_thesis_paragraphs.append(elaborated)

#     #         # Regenerate investment thesis full text from all paragraphs
#     #         self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)

#     #         # Regenerate the full PDF
#     #         self.pdf_generated_bytes, pdf_error = generate_styled_pdf(
#     #             self.company_name,
#     #             self.llm_business_overview or "",
#     #             self.llm_quarterly_highlights or "",
#     #             self.llm_investment_thesis or "",
#     #         )

#     #         return {
#     #             "added_point": prompt,
#     #             "elaborated_text": elaborated,
#     #             "pdf_error": pdf_error if pdf_error else None
#     #         }

#     #     except Exception as e:
#     #         return {
#     #             "added_point": prompt,
#     #             "elaborated_text": "",
#     #             "error": str(e)
#     #         }
#     def add_thesis_point(self, prompt: str) -> Dict:
#         """
#         Add a new thesis point, elaborate it using the RAG pipeline, and update the PDF report in real-time.
#         """
#         try:
#             # 1️⃣ Save the thesis point
#             self.key_thesis_points.append(prompt)

#             # 2️⃣ Elaborate on the thesis point using RAG
#             elaborated_text, sources, error = elaborate_on_thesis_point(
#                 prompt,             # Positional arg instead of point=
#                 200,
#                 self.vectordb,
#                 self.num_docs
#             )

#             if error:
#                 return {
#                     "status": "error",
#                     "added_point": prompt,
#                     "elaborated_text": "",
#                     "sources": [],
#                     "pdf_base64": None,
#                     "error": error
#                 }

#             # 3️⃣ Append elaborated text to full investment thesis
#             self.current_thesis_paragraphs.append(elaborated_text)
#             self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)

#             # 4️⃣ Regenerate the PDF
#             self.pdf_generated_bytes, pdf_error = generate_styled_pdf(
#                 self.company_name,
#                 self.llm_business_overview or "",
#                 self.llm_quarterly_highlights or "",
#                 self.llm_investment_thesis or "",
#             )

#             pdf_base64 = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode("utf-8") \
#                 if self.pdf_generated_bytes else None

#             return {
#                 "status": "success",
#                 "added_point": prompt,
#                 "elaborated_text": elaborated_text,
#                 "sources": format_sources_for_display(sources),
#                 "pdf_base64": pdf_base64,
#                 "error": pdf_error
#             }

#         except Exception as e:
#             return {
#                 "status": "error",
#                 "added_point": prompt,
#                 "elaborated_text": "",
#                 "sources": [],
#                 "pdf_base64": None,
#                 "error": str(e)
#             }



#     # def elaborate_on_thesis_point(point_summary: str, word_count: int, vectordb, num_docs: int) -> Tuple[str, Optional[str]]:
#     #     result = {
#     #         "status": "success",
#     #         "detailed_point": "",
#     #         "sources": [],
#     #         "errors": []
#     #     }

#     #     try:
#     #         detailed_text, sources, error = elaborate_on_thesis_point(vectordb, point_summary, num_docs, word_count)
#     #         result["detailed_point"] = detailed_text
#     #         result["sources"] = format_sources_for_display(sources)
#     #         if error:
#     #             result["errors"].append(error)
#     #     except Exception as e:
#     #         result.update({"status": "error", "errors": [f"Error elaborating thesis point: {str(e)}"]})

#     #     return result
#     def elaborate_on_thesis_point(
#         point_summary: str,
#         word_count: int,
#         vectordb,
#         num_docs: int
#     ) -> Tuple[str, list, Optional[str]]:
#         """
#         Elaborate on a thesis point using the vector store and LLM.
#         Returns:
#             (elaborated_text, source_documents, error_message)
#         """
#         try:
#             # Validate Google API Key
#             if not GOOGLE_API_KEY:
#                 return "", [], "Google API key is missing or invalid."

#             # Validate vector store
#             if vectordb is None:
#                 return "", [], "Vector store is not initialized. Please analyze documents first."

#             # Setup LLM
#             llm = ChatGoogleGenerativeAI(
#                 model="gemini-2.5-flash",
#                 google_api_key=GOOGLE_API_KEY,
#                 temperature=0.0,
#             )

#             # Retrieve documents related to the thesis point
#             k_value = min(30, num_docs) if num_docs > 0 else 1
#             retriever = MultiQueryRetriever.from_llm(
#                 retriever=vectordb.as_retriever(search_kwargs={"k": k_value}),
#                 llm=llm
#             )
#             retrieved_docs = retriever.invoke(point_summary)

#             # Prompt for elaboration
#             prompt_template = PromptTemplate.from_template(
#                 """
#                 You are a senior equity research analyst. Using ONLY the provided context, expand on the following investment thesis point into a detailed paragraph (~{word_count} words).
#                 Maintain a professional and analytical tone. Do NOT invent data.

#                 Thesis Point:
#                 {point_summary}

#                 Context:
#                 {context}

#                 Elaborated Thesis Point:
#                 """
#             )

#             document_chain = create_stuff_documents_chain(llm, prompt_template)
#             rag_chain = (
#                 {
#                     "context": retrieved_docs,
#                     "point_summary": RunnablePassthrough()
#                 }
#                 | document_chain
#             )

#             response = rag_chain.invoke({
#                 "point_summary": point_summary,
#                 "word_count": word_count
#             })

#             elaborated_text = add_inline_citations(response.strip(), retrieved_docs)
#             return elaborated_text, retrieved_docs, None

#         except Exception as e:
#             return "", [], f"Error during elaboration: {str(e)}"

    
#     def adjust_thesis_length(self, index: int, word_count: int) -> Dict:
#         """
#         Adjusts the word count of an existing key thesis point's elaboration in the Investment Thesis section.
#         This applies only to the individual elaborated point, not the entire thesis.
#         """
#         if index < 0 or index >= len(self.key_thesis_points):
#             return {"error": "Invalid key thesis point index"}

#         try:
#             thesis_point = self.key_thesis_points[index]

#             # Re-elaborate the thesis point with the new word count
#             elaborated, error = elaborate_on_thesis_point(
#                 point_summary=thesis_point,
#                 word_count=word_count,
#                 vectordb=self.vectordb,
#                 num_docs=self.num_docs
#             )

#             if error:
#                 return {"error": error}

#             # Update the corresponding paragraph in Investment Thesis
#             if index < len(self.current_thesis_paragraphs):
#                 self.current_thesis_paragraphs[index] = elaborated
#             else:
#                 self.current_thesis_paragraphs.append(elaborated)

#             return {
#                 "index": index,
#                 "adjusted_text": elaborated
#             }

#         except Exception as e:
#             return {"error": str(e)}



# def detect_units_in_text(text: str) -> Dict[str, str]:
#     if not text:
#         return {}
#     units = {}
#     patterns = {
#         "%": r"\d+\.?\d*%", "~": r"~\d+", "$": r"\$\d+\.?\d*",
#         "(Y/Y)": r"\(Y/Y\)", "€": r"€\d+\.?\d*", "million": r"\d+\.?\d*\s*million",
#         "<": r"<\d+\.?\d*", ">": r">\d+\.?\d*"
#     }
#     for unit, pattern in patterns.items():
#         if re.search(pattern, text, re.IGNORECASE):
#             units[unit] = patterns[unit]
#     return units



####################################################################################################################################


import os
import io
import base64
import hashlib
import re 
import time
from typing import List, Dict, Tuple, Set, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from operator import itemgetter
import torch
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import PromptTemplate
from rag_pipeline import (
    clean_company_name, extract_text_from_pdfs, create_faiss_vectorstore, get_company_name_from_llm,
    extract_company_name_fallback_regex, generate_styled_pdf, modify_report_section,
    validate_and_rerun_quarterly_earnings, extract_key_thesis_points, elaborate_on_thesis_point,
    format_sources_for_display, convert_units,add_inline_citations
)

from prompt_templates import (
    get_business_overview_prompt_template, get_quarterly_earnings_prompt_template,
    get_investment_thesis_prompt_template, get_key_thesis_points_prompt_template, 
    get_detailed_explanation_prompt_template,get_chat_prompt_template
)
 
# Set torch path to avoid issues 
torch.classes.__path__ = []

import nltk
nltk.download('punkt', quiet=True)

# --- Global Variables & Constants ---
DEFAULT_COMPANY_NAME = "Company Analysis Report"
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class FinanceBot:
    def load_chat_history(self):
        if not self.session_id:
            return []
        return self.session_data.get(f"chat_history_{self.session_id}", [])

    def save_chat_history(self, history):
        if self.session_id:
            self.session_data[f"chat_history_{self.session_id}"] = history

    def __init__(self, session_id=None):
        self.session_id = session_id
        self.session_data = {}
        self.chat_history = self.load_chat_history() if session_id else []
        self.company_name = DEFAULT_COMPANY_NAME
        self.vectordb = None
        self.num_docs = 0
        self.raw_text = ""
        self.llm_business_overview = ""
        self.llm_quarterly_highlights = ""
        self.llm_investment_thesis = ""
        self.business_overview_sources = []
        self.quarterly_highlights_sources = []
        self.investment_thesis_sources = []
        self.global_references: Set[str] = set()
        self.global_citation_details_map: Dict[str, str] = {}
        self.global_citation_details_list: List[Dict] = []
        self.key_thesis_points = []
        self.current_thesis_paragraphs = []
        self.pdf_generated_bytes: Optional[io.BytesIO] = None
        self.detected_units = {}
        self.custom_unit_mappings = {
            "%": "percentage", "~": "approximately", "$": "US dollar", "(Y/Y)": "year-on-year",
            "€": "Euro", "million": "M", "<": "less than", ">": "greater than",
            "Euro": "€", "USD": "$"
        }
        self.llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash", 
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2, 
            top_p=0.8,       
            top_k=40)   
    def chat(
        self,
        files: List[str],
        query: str,
        history: List[Dict[str, str]],
        file_objects: Optional[List[io.BytesIO]] = None
    ) -> str:
        """
        Process a user query using the RAG pipeline and return a response with inline citations.

        Args:
            files (List[str]): Filenames selected by the user.
            query (str): User's query.
            history (List[Dict[str, str]]): Chat history.
            file_objects (Optional[List[BytesIO]]): Corresponding file buffers.

        Returns:
            str: Response HTML with inline citations.
        """
        if not self.vectordb:
            if not files or not file_objects:
                return "No context available to answer the query. Please upload relevant files."

            if len(file_objects) != len(files):
                return "Mismatch between filenames and file objects."

            all_docs, raw_text, _, error = extract_text_from_pdfs(file_objects)
            if error or not all_docs:
                return f"Error extracting text from files: {error or 'No text extracted'}"

            self.raw_text = raw_text
            self.num_docs = len(all_docs)
            self.vectordb, _, error = create_faiss_vectorstore(all_docs)
            if error or self.vectordb is None:
                return f"Error creating vector store: {error or 'Vector store creation failed'}"

        # Load chat prompt
        chat_prompt_template = get_chat_prompt_template()

        # Format chat history
        formatted_history = ""
        for msg in history:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")
            formatted_history += f"{role}: {content}\n"

        try:
            retriever = MultiQueryRetriever.from_llm(
                retriever=self.vectordb.as_retriever(search_kwargs={"k": 10}),
                llm=self.llm
            )
        except Exception as e:
            return f"Error initializing retriever: {str(e)}"

        doc_chain = create_stuff_documents_chain(self.llm, chat_prompt_template)
        rag_chain = (
            {
                "context": retriever,
                "query": RunnablePassthrough(),
                "history": lambda x: formatted_history
            }
            | doc_chain
        )

        try:
            response = rag_chain.invoke(query)
            retrieved_docs = retriever.invoke(query)
            response_with_citations = add_inline_citations(response, retrieved_docs)
            return response_with_citations  # ✅ Raw HTML string ready for frontend rendering
        except Exception as e:
            return f"Error processing query: {str(e)}"

    # def chat(self, files: List[str], query: str, history: List[Dict[str, str]], file_objects: Optional[List[io.BytesIO]] = None) -> Tuple[str, List[str]]:
    #     """
    #     Process a user query using the RAG pipeline and return a response with sources.
        
    #     Args:
    #         files (List[str]): List of filenames to use for context.
    #         query (str): User's query or question.
    #         history (List[Dict[str, str]]): Chat history containing user and assistant messages.
    #         file_objects (Optional[List[io.BytesIO]]): List of file objects corresponding to filenames, if available.
        
    #     Returns:
    #         Tuple[str, List[str]]: The generated response and a list of formatted source references.
    #     """
    #     if not self.vectordb:
    #         if not files or not file_objects:
    #             return "No context available to answer the query. Please upload relevant files.", []
            
    #         if len(file_objects) != len(files):
    #             return "Mismatch between filenames and file objects.", []
            
    #         # Extract text from file objects with proper tuple handling
    #         all_docs, raw_text, _, error = extract_text_from_pdfs(file_objects)
    #         if error or not all_docs:
    #             return f"Error extracting text from files: {error or 'No text extracted'}", []
            
    #         self.raw_text = raw_text
    #         self.num_docs = len(all_docs)
            
    #         # Create vector store with error handling
    #         self.vectordb, _, error = create_faiss_vectorstore(all_docs)
    #         if error or self.vectordb is None:
    #             return f"Error creating vector store: {error or 'Vector store creation failed'}", []

    #     # Define a prompt template for the chat query
    #     chat_prompt_template = PromptTemplate.from_template(
    #         """
    #         You are a financial analyst assistant. Use the provided context to answer the user's query accurately and concisely.
    #         Incorporate relevant information from the chat history if applicable.
    #         If specific details are not available in the context, clearly state so and provide a general response if possible.
            
    #         Chat History:
    #         {history}
            
    #         Context:
    #         {context}
            
    #         Query:
    #         {query}
            
    #         Answer:
    #         """
    #     )

    #     # Format chat history for the prompt
    #     formatted_history = ""
    #     for msg in history:
    #         role = msg.get("role", "").capitalize()
    #         content = msg.get("content", "")
    #         formatted_history += f"{role}: {content}\n"
        
    #     # Set up the retriever
    #     try:
    #         retriever = MultiQueryRetriever.from_llm( 
    #             retriever=self.vectordb.as_retriever(search_kwargs={"k": 10}),
    #             llm=self.llm
    #         )
    #     except Exception as e:
    #         return f"Error initializing retriever: {str(e)}", []

    #     # Create the document chain
    #     doc_chain = create_stuff_documents_chain(self.llm, chat_prompt_template)

    #     # Set up the RAG chain
    #     rag_chain = (
    #         {
    #             "context": retriever,
    #             "query": RunnablePassthrough(),
    #             "history": lambda x: formatted_history
    #         }
    #         | doc_chain
    #     )

    #     # Execute the query
    #     try:
    #         response = rag_chain.invoke(query)
    #         retrieved_docs = retriever.invoke(query) 
    #         #sources = format_sources_for_display(retrieved_docs, self.global_references, self.global_citation_details_map)
    #         #ources = format_sources_for_display(retrieved_docs)
    #         # response, detected_units = convert_units(response, self.custom_unit_mappings)
    #         # self.detected_units.update(detected_units)
            
    #         response = add_inline_citations(response, retrieved_docs)
    #         return response 
    #     except Exception as e:
    #         return f"Error processing query: {str(e)}", []

    def analyze_documents(self, uploaded_files: List[io.BytesIO], file_names: List[str]) -> Dict:
        """
        Analyze uploaded PDF documents and generate insights.
        """
        result = {
            "status": "success",
            "company_name": self.company_name,
            "business_overview": "",
            "quarterly_highlights": "",
            "investment_thesis": "",
            "key_thesis_points": [],
            "pdf_bytes": None,
            "references": [],
            "errors": []
        }

        # Reset internal state
        self.vectordb = None
        self.num_docs = 0
        self.raw_text = ""
        self.llm_business_overview = ""
        self.llm_quarterly_highlights = ""
        self.llm_investment_thesis = ""
        self.business_overview_sources = []
        self.quarterly_highlights_sources = []
        self.investment_thesis_sources = []
        self.global_references = set()
        self.global_citation_details_map = {}
        self.global_citation_details_list = []
        self.key_thesis_points = []
        self.current_thesis_paragraphs = []

        if not uploaded_files:
            result.update({
                "status": "error",
                "errors": ["No files uploaded. Please provide PDF documents."],
                "business_overview": "No text extracted from PDFs.",
                "quarterly_highlights": "No text extracted from PDFs.",
                "investment_thesis": "No text extracted from PDFs."
            })
            return result

        # Extract text from PDFs
        all_docs, raw_text, _, error = extract_text_from_pdfs(uploaded_files)
        self.raw_text = raw_text

        if error or not all_docs:
            result.update({
                "status": "error",
                "errors": [error or "Could not extract any text from the uploaded PDF files."],
                "business_overview": "No text extracted from PDFs.",
                "quarterly_highlights": "No text extracted from PDFs.",
                "investment_thesis": "No text extracted from PDFs."
            })
            return result

        # Create vector store
        self.vectordb, self.num_docs, error = create_faiss_vectorstore(all_docs)
        if error:
            result.update({
                "status": "error",
                "errors": [error],
                "business_overview": "Vector store error prevented analysis.",
                "quarterly_highlights": "Vector store error prevented analysis.",
                "investment_thesis": "Vector store error prevented analysis."
            })
            return result

        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.0,
        )

        # Extract company name
        self.company_name = get_company_name_from_llm(llm, self.raw_text, file_names)
        if self.company_name == DEFAULT_COMPANY_NAME:
            self.company_name = extract_company_name_fallback_regex(self.raw_text, file_names)
        result["company_name"] = self.company_name

        # Generate Business Overview
        try:
            k_value = min(50, self.num_docs) if self.num_docs > 0 else 1
            retriever = MultiQueryRetriever.from_llm(
                retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
            )
            chain = create_stuff_documents_chain(llm, get_business_overview_prompt_template())
            rag = (
                RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
                | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
            )
            time.sleep(3)
            response = rag.invoke({
                "input": f"Generate a detailed business overview of {self.company_name} based on its core business, revenue segments (with percentages) and what each segment encompasses, geographic distribution (with percentages), headquarters, stock exchange with its names, and employee count."
            })
            self.llm_business_overview = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))
            self.business_overview_sources = response.get("source_documents", [])
            result["business_overview"] = self.llm_business_overview
            if not self.llm_business_overview or len(self.llm_business_overview) < 50 or \
               any(keyword in self.llm_business_overview.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
                result["errors"].append("Business Overview: Insufficient data detected.")
        except Exception as e:
            result["errors"].append(f"Error generating Business Overview: {str(e)}")
            self.llm_business_overview = "Error generating business overview."
            result["business_overview"] = self.llm_business_overview

        # Generate Quarterly Earnings
        try:
            k_value = min(50, self.num_docs) if self.num_docs > 0 else 1
            retriever = MultiQueryRetriever.from_llm(
                retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
            )
            chain = create_stuff_documents_chain(llm, get_quarterly_earnings_prompt_template())
            rag = (
                RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
                | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
            )
            time.sleep(3)
            response = rag.invoke({
                "input": f"For {self.company_name}, compare the financial performance of Q1 2025 with Q1 2024, including revenue, EBIT, adjusted EBIT, margin with y/y changes, and full-year 2025 outlook."
            })
            self.llm_quarterly_highlights = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))      
            initial_quarterly_highlights = response["answer"].strip()
            self.quarterly_highlights_sources = response.get("source_documents", [])
            annotated_text, sources, error = validate_and_rerun_quarterly_earnings(
                self.vectordb, self.company_name, initial_quarterly_highlights, self.num_docs
            )
            self.llm_quarterly_highlights = annotated_text
            if sources:
                self.quarterly_highlights_sources = sources
            result["quarterly_highlights"] = self.llm_quarterly_highlights
            if error:
                result["errors"].append(error)
        except Exception as e:
            result["errors"].append(f"Error generating Quarterly Highlights: {str(e)}")
            self.llm_quarterly_highlights = "Error generating quarterly highlights."
            result["quarterly_highlights"] = self.llm_quarterly_highlights

        # Generate Investment Thesis
        try:
            k_value = min(50, self.num_docs) if self.num_docs > 0 else 1
            retriever = MultiQueryRetriever.from_llm(
                retriever=self.vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm
            )
            chain = create_stuff_documents_chain(llm, get_investment_thesis_prompt_template())
            rag = (
                RunnableParallel({"context": itemgetter("input") | retriever, "input": RunnablePassthrough()})
                | RunnableParallel({"answer": chain, "source_documents": itemgetter("context")})
            )
            time.sleep(3)
            response = rag.invoke({
                "input": f"Construct a detailed investment thesis for {self.company_name}."
            })
            self.llm_investment_thesis = add_inline_citations(response["answer"].strip(), response.get("source_documents", []))
            self.investment_thesis_sources = response.get("source_documents", [])
            self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]
            result["investment_thesis"] = self.llm_investment_thesis
            if not self.llm_investment_thesis or len(self.llm_investment_thesis) < 50 or \
               any(keyword in self.llm_investment_thesis.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
                result["errors"].append("Investment Thesis: Insufficient data detected.")
        except Exception as e:
            result["errors"].append(f"Error generating Investment Thesis: {str(e)}")
            self.llm_investment_thesis = "Error generating investment thesis."
            result["investment_thesis"] = self.llm_investment_thesis

        # Extract Key Thesis Points
        try:
            self.key_thesis_points, error = extract_key_thesis_points(vectordb=self.vectordb, num_docs=self.num_docs)
            result["key_thesis_points"] = self.key_thesis_points
            if error:
                result["errors"].append(error)
        except Exception as e:
            result["errors"].append(f"Error extracting key thesis points: {str(e)}")

        # Generate PDF
        try:
            self.pdf_generated_bytes, error =  generate_styled_pdf(
                self.company_name,
                self.llm_business_overview or "",
                self.llm_quarterly_highlights or "", 
                self.llm_investment_thesis or "",
                
            )
            #result["pdf_bytes"] = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None
            result["pdf_bytes"] = self.pdf_generated_bytes
            if error:
                result["errors"].append(error) 
        except Exception as e:
            result["errors"].append(f"Error generating PDF: {str(e)}")

        # Detect units 
        combined_text = f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}"
        self.detected_units = detect_units_in_text(combined_text)
        result["detected_units"] = self.detected_units

        return result
    
    def get_result(self) -> Dict:
        """
        Return the current state of the report and the latest PDF.
        """
        pdf_base64 = None
        if self.pdf_generated_bytes:
            pdf_base64 = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode("utf-8")
        
        return {
            "company_name": self.company_name,
            "business_overview": self.llm_business_overview,
            "quarterly_highlights": self.llm_quarterly_highlights,
            "investment_thesis": self.llm_investment_thesis,
            "key_thesis_points": self.key_thesis_points,
            "pdf_base64": pdf_base64,
        }


    def apply_unit_conversion(self, conversion_profile: str, custom_mappings: Optional[Dict[str, str]] = None) -> Dict:
        result = {
            "status": "success",
            "business_overview": "",
            "quarterly_highlights": "",
            "investment_thesis": "",
            "pdf_bytes": None,
            "errors": []
        }

        custom_mappings = custom_mappings or self.custom_unit_mappings
        try:
            if self.llm_business_overview:
                self.llm_business_overview = convert_units(self.llm_business_overview, conversion_profile, custom_mappings)
            if self.llm_quarterly_highlights:
                self.llm_quarterly_highlights = convert_units(self.llm_quarterly_highlights, conversion_profile, custom_mappings)
            if self.llm_investment_thesis:
                self.llm_investment_thesis = convert_units(self.llm_investment_thesis, conversion_profile, custom_mappings)
                self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]

            self.pdf_generated_bytes, error = generate_styled_pdf(
                self.company_name,
                self.llm_business_overview or "",
                self.llm_quarterly_highlights or "",
                self.llm_investment_thesis or "",
                
            )
            result.update({
                "business_overview": self.llm_business_overview,
                "quarterly_highlights": self.llm_quarterly_highlights,
                "investment_thesis": self.llm_investment_thesis,
                "pdf_bytes": base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None,
                "detected_units": detect_units_in_text(f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}")
            })
            if error:
                result["errors"].append(error)
        except Exception as e:
            result.update({
                "status": "error",
                "errors": [f"Error applying unit conversion: {str(e)}"]
            })

        return result

    def modify_report(self, section: str, modification_prompt: str) -> Dict:
        result = {
            "status": "success",
            "modified_section": "",
            "section_name": section,
            "sources": [],
            "pdf_bytes": None,
            "errors": []
        }

        if not modification_prompt:
            result.update({"status": "error", "errors": ["Modification prompt is required."]})
            return result

        current_content = ""
        if section.lower() in ["business overview", "overview"]:
            current_content = self.llm_business_overview
        elif section.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
            current_content = self.llm_quarterly_highlights
        elif section.lower() in ["investment thesis", "thesis"]:
            current_content = self.llm_investment_thesis
        else:
            result.update({"status": "error", "errors": [f"Invalid section: {section}"]})
            return result

        try:
            modified_text_annotated, sources, error = modify_report_section(
                self.vectordb,
                modification_prompt,
                section,
                self.company_name,
                self.num_docs,
                current_content
            )
            if modified_text_annotated:
                if section.lower() in ["business overview", "overview"]:
                    self.llm_business_overview = modified_text_annotated
                    self.business_overview_sources = sources
                    result["modified_section"] = self.llm_business_overview
                elif section.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
                    self.llm_quarterly_highlights = modified_text_annotated
                    self.quarterly_highlights_sources = sources
                    result["modified_section"] = self.llm_quarterly_highlights
                elif section.lower() in ["investment thesis", "thesis"]:
                    self.llm_investment_thesis = modified_text_annotated
                    self.investment_thesis_sources = sources
                    self.current_thesis_paragraphs = [p.strip() for p in self.llm_investment_thesis.split('\n\n') if p.strip()]
                    self.key_thesis_points, error = extract_key_thesis_points(self.vectordb, self.num_docs)
                    result["modified_section"] = self.llm_investment_thesis
                    result["key_thesis_points"] = self.key_thesis_points
                    if error:
                        result["errors"].append(error)

                self.pdf_generated_bytes, error = generate_styled_pdf(
                    self.company_name,
                    self.llm_business_overview or "",
                    self.llm_quarterly_highlights or "",
                    self.llm_investment_thesis or "",
                    
                )
                result["pdf_bytes"] = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode('utf-8') if self.pdf_generated_bytes else None
                result["sources"] = format_sources_for_display(sources)
                result["detected_units"] = detect_units_in_text(f"{self.llm_business_overview}\n{self.llm_quarterly_highlights}\n{self.llm_investment_thesis}")
                if error:
                    result["errors"].append(error)
            else:
                result.update({"status": "error", "errors": ["Failed to modify the section."]})
        except Exception as e:
            result.update({"status": "error", "errors": [f"Error modifying {section}: {str(e)}"]})

        return result
    def edit_thesis_point(self, index: int, action: str, prompt: Optional[str] = None) -> Dict:
        if not (0 <= index < len(self.current_thesis_paragraphs)):
            return {"status": "error", "message": "Invalid index for thesis paragraph."}
        
        if action == "delete":
            self.current_thesis_paragraphs.pop(index)
        # elif action == "rewrite":
        #     if not prompt:
        #         return {"status": "error", "message": "Rewrite requires a prompt."}
        #     self.current_thesis_paragraphs[index] = prompt
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}

        self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)
        
        self.pdf_generated_bytes, pdf_error = generate_styled_pdf(
                self.company_name,
                self.llm_business_overview or "",
                self.llm_quarterly_highlights or "",
                self.llm_investment_thesis or "",
            )

        pdf_base64 = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode("utf-8") \
            if self.pdf_generated_bytes else None
        return {
            "updated_thesis": self.llm_investment_thesis,
            "key_thesis_points": self.key_thesis_points,
            "pdf_base64": pdf_base64,
            "pdf_error": pdf_error
        }

  
    # def add_thesis_point(self, prompt: str) -> Dict:
    
    #     try:
    #         # Save the key thesis point
    #         self.key_thesis_points.append(prompt)

    #         # Elaborate the point using default 200 words
    #         elaborated, error = elaborate_on_thesis_point(
    #             point=prompt,
    #             word_count=200,
    #             vectordb=self.vectordb,
    #             num_docs=self.num_docs
    #         )

    #         if error:
    #             return {
    #                 "added_point": prompt,
    #                 "elaborated_text": "",
    #                 "error": error
    #             }

    #         # Append to thesis paragraphs
    #         self.current_thesis_paragraphs.append(elaborated)

    #         # Regenerate investment thesis full text from all paragraphs
    #         self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)

    #         # Regenerate the full PDF
    #         self.pdf_generated_bytes, pdf_error = generate_styled_pdf(
    #             self.company_name,
    #             self.llm_business_overview or "",
    #             self.llm_quarterly_highlights or "",
    #             self.llm_investment_thesis or "",
    #         )

    #         return {
    #             "added_point": prompt,
    #             "elaborated_text": elaborated,
    #             "pdf_error": pdf_error if pdf_error else None
    #         }

    #     except Exception as e:
    #         return {
    #             "added_point": prompt,
    #             "elaborated_text": "",
    #             "error": str(e)
    #         }
    def add_thesis_point(self, prompt: str) -> Dict:
        """
        Add a new thesis point, elaborate it using the RAG pipeline, and update the PDF report in real-time.
        """
        try:
            # 1️⃣ Save the thesis point
            self.key_thesis_points.append(prompt)

            # 2️⃣ Elaborate on the thesis point using RAG
            elaborated_text, sources, error = elaborate_on_thesis_point(
                prompt,             # Positional arg instead of point=
                200,
                self.vectordb,
                self.num_docs
            )

            if error:
                return {
                    "status": "error",
                    "added_point": prompt,
                    "elaborated_text": "",
                    "sources": [],
                    "pdf_base64": None,
                    "error": error
                }

            # 3️⃣ Append elaborated text to full investment thesis
            self.current_thesis_paragraphs.append(elaborated_text)
            self.llm_investment_thesis = "\n\n".join(self.current_thesis_paragraphs)

            # 4️⃣ Regenerate the PDF
            self.pdf_generated_bytes, pdf_error = generate_styled_pdf(
                self.company_name,
                self.llm_business_overview or "",
                self.llm_quarterly_highlights or "",
                self.llm_investment_thesis or "",
            )

            pdf_base64 = base64.b64encode(self.pdf_generated_bytes.getvalue()).decode("utf-8") \
                if self.pdf_generated_bytes else None

            return {
                "status": "success",
                "added_point": prompt,
                "elaborated_text": elaborated_text,
                "sources": format_sources_for_display(sources),
                "pdf_base64": pdf_base64,
                "error": pdf_error
            }

        except Exception as e:
            return {
                "status": "error",
                "added_point": prompt,
                "elaborated_text": "",
                "sources": [],
                "pdf_base64": None,
                "error": str(e)
            }



    # def elaborate_on_thesis_point(point_summary: str, word_count: int, vectordb, num_docs: int) -> Tuple[str, Optional[str]]:
    #     result = {
    #         "status": "success",
    #         "detailed_point": "",
    #         "sources": [],
    #         "errors": []
    #     }

    #     try:
    #         detailed_text, sources, error = elaborate_on_thesis_point(vectordb, point_summary, num_docs, word_count)
    #         result["detailed_point"] = detailed_text
    #         result["sources"] = format_sources_for_display(sources)
    #         if error:
    #             result["errors"].append(error)
    #     except Exception as e:
    #         result.update({"status": "error", "errors": [f"Error elaborating thesis point: {str(e)}"]})

    #     return result
    def elaborate_on_thesis_point(
        point_summary: str,
        word_count: int,
        vectordb,
        num_docs: int
    ) -> Tuple[str, list, Optional[str]]:
        """
        Elaborate on a thesis point using the vector store and LLM.
        Returns:
            (elaborated_text, source_documents, error_message)
        """
        try:
            # Validate Google API Key
            if not GOOGLE_API_KEY:
                return "", [], "Google API key is missing or invalid."

            # Validate vector store
            if vectordb is None:
                return "", [], "Vector store is not initialized. Please analyze documents first."

            # Setup LLM
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.0,
            )

            # Retrieve documents related to the thesis point
            k_value = min(30, num_docs) if num_docs > 0 else 1
            retriever = MultiQueryRetriever.from_llm(
                retriever=vectordb.as_retriever(search_kwargs={"k": k_value}),
                llm=llm
            )
            retrieved_docs = retriever.invoke(point_summary)

            # Prompt for elaboration
            prompt_template = PromptTemplate.from_template(
                """
                You are a senior equity research analyst. Using ONLY the provided context, expand on the following investment thesis point into a detailed paragraph (~{word_count} words).
                Maintain a professional and analytical tone. Do NOT invent data.

                Thesis Point:
                {point_summary}

                Context:
                {context}

                Elaborated Thesis Point:
                """
            )

            document_chain = create_stuff_documents_chain(llm, prompt_template)
            rag_chain = (
                {
                    "context": retrieved_docs,
                    "point_summary": RunnablePassthrough()
                }
                | document_chain
            )

            response = rag_chain.invoke({
                "point_summary": point_summary,
                "word_count": word_count
            })

            elaborated_text = add_inline_citations(response.strip(), retrieved_docs)
            return elaborated_text, retrieved_docs, None

        except Exception as e:
            return "", [], f"Error during elaboration: {str(e)}"

    
    def adjust_thesis_length(self, index: int, word_count: int) -> Dict:
        """
        Adjusts the word count of an existing key thesis point's elaboration in the Investment Thesis section.
        This applies only to the individual elaborated point, not the entire thesis.
        """
        if index < 0 or index >= len(self.key_thesis_points):
            return {"error": "Invalid key thesis point index"}

        try:
            thesis_point = self.key_thesis_points[index]

            # Re-elaborate the thesis point with the new word count
            elaborated, error = elaborate_on_thesis_point(
                point_summary=thesis_point,
                word_count=word_count,
                vectordb=self.vectordb,
                num_docs=self.num_docs
            )

            if error:
                return {"error": error}

            # Update the corresponding paragraph in Investment Thesis
            if index < len(self.current_thesis_paragraphs):
                self.current_thesis_paragraphs[index] = elaborated
            else:
                self.current_thesis_paragraphs.append(elaborated)

            return {
                "index": index,
                "adjusted_text": elaborated
            }

        except Exception as e:
            return {"error": str(e)}



def detect_units_in_text(text: str) -> Dict[str, str]:
    if not text:
        return {}
    units = {}
    patterns = {
        "%": r"\d+\.?\d*%", "~": r"~\d+", "$": r"\$\d+\.?\d*",
        "(Y/Y)": r"\(Y/Y\)", "€": r"€\d+\.?\d*", "million": r"\d+\.?\d*\s*million",
        "<": r"<\d+\.?\d*", ">": r">\d+\.?\d*"
    }
    for unit, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            units[unit] = patterns[unit]
    return units
 