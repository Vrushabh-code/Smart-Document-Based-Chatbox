# import os
# from typing import Optional, Tuple
# from dotenv import load_dotenv
# import re
# from datetime import datetime
# from io import BytesIO
# import html
# import torch
# import time
# import pdfplumber
# from sentence_transformers import SentenceTransformer, util
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.prompts import PromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.documents import Document
# from langchain.schema import Document
# from langchain.retrievers import MultiQueryRetriever
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough, RunnableParallel
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import inch
# from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
# from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate
# from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
# import nltk

# # Placeholder for prompt templates (replace with actual templates)
# from prompt_templates import (
#     get_business_overview_prompt_template,
#     get_detailed_explanation_prompt_template,
#     get_investment_thesis_prompt_template,
#     get_key_thesis_points_prompt_template,
#     get_quarterly_earnings_prompt_template
# ) 

# # Configuration
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# DEFAULT_COMPANY_NAME = "Company Analysis Report"

# # Initialize SentenceTransformer model
# sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
# torch.classes.__path__ = []

# # Session state equivalent for citation management and caching
# class SessionState:
#     def __init__(self):
#         self.global_citation_details_list = []
#         self.global_citation_details_map = {}
#         self.global_references = set()
#         self.processed_file_hashes = []
#         self.cache = {}

# session_state = SessionState()

# def extract_text_from_pdfs(uploaded_files):
#     """
#     Extracts text and tables from uploaded PDF files.
#     Args:
#         uploaded_files: List of file objects (e.g., from file upload).
#     Returns:
#         Tuple: (list of Document objects, raw concatenated text, list of file names, error message if any).
#     """
#     all_docs = []
#     file_names = []
#     raw_texts = []
    
#     for file in uploaded_files:
#         file_names.append(file.name)
#         try:
#             with pdfplumber.open(file) as pdf:
#                 for page_num, page in enumerate(pdf.pages):
#                     text = page.extract_text() or ""
#                     tables = page.extract_tables()
#                     if text.strip():
#                         all_docs.append(Document(
#                             page_content=text,
#                             metadata={"source": file.name, "page": page_num + 1, "type": "text"}
#                         ))
#                         raw_texts.append(text)
#                     table_text_parts = []
#                     for table in tables:
#                         for row in table:
#                             table_text_parts.append(" | ".join(map(lambda x: str(x) if x is not None else "", row)))
#                     table_text = "\n".join(table_text_parts)
#                     if table_text.strip():
#                         all_docs.append(Document(
#                             page_content=table_text,
#                             metadata={"source": file.name, "page": page_num + 1, "type": "table"}
#                         ))
#                         raw_texts.append(table_text)
#         except Exception as e:
#             return None, None, None, f"Error processing PDF {file.name}: {str(e)}"
#     raw_text_for_all_docs = "\n\n".join(raw_texts)
#     return all_docs, raw_text_for_all_docs, file_names, None

# def create_faiss_vectorstore(documents):
#     """
#     Creates a FAISS vector store from the provided documents.
#     Args:
#         documents: List of Document objects.
#     Returns:
#         Tuple: (FAISS vector store, number of documents, error message if any).
#     """
#     if not documents:
#         return None, 0, "No documents provided to create vector store."
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=4000,
#         chunk_overlap=1000
#     )
#     docs_for_vectorstore = splitter.split_documents(documents)
#     if not docs_for_vectorstore:
#         return None, 0, "Document splitting resulted in no documents."
#     num_docs = len(docs_for_vectorstore)
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     try:
#         vectordb = FAISS.from_documents(docs_for_vectorstore, embeddings)
#         return vectordb, num_docs, None
#     except Exception as e:
#         return None, 0, f"Error creating FAISS vector store: {str(e)}"

# def clean_html_for_pdf(text_with_html):
#     """
#     Removes citation-related HTML tags from the text for PDF generation.
#     Args:
#         text_with_html: Text containing HTML tags.
#     Returns:
#         Cleaned text without HTML citation tags.
#     """
#     cleaned = re.sub(r'<sup[^>]*?>.*?</sup>', '', text_with_html)
#     return cleaned

# def add_inline_citations(text, source_documents): 
#     """
#     Adds inline citations to the provided text based on source documents.
#     Updates global citation state in session_state.
#     Args:
#         text: Input text to annotate with citations.
#         source_documents: List of Document objects for citation sources.
#     Returns:
#         Text with inline citation HTML tags.
#     """
#     nltk.download('punkt', quiet=True)
#     from nltk.tokenize import sent_tokenize

#     def _get_citation_info(source_file, page, raw_context_snippet, data_type):
#         display_context_escaped = html.escape(raw_context_snippet)
#         if len(display_context_escaped) > 250:
#             display_context_escaped = display_context_escaped[:250] + "..."
#         citation_detail_html = (
#             f"<div class='citation-field'><strong>Source:</strong> {html.escape(source_file)}</div>"
#             f"<div class='citation-field'><strong>Page:</strong> {html.escape(str(page))}</div>"
#             f"<div class='citation-field'><strong>Type:</strong> {html.escape(data_type.capitalize())}</div>"
#             f"<div class='citation-field'><strong>Context:</strong> {display_context_escaped}</div>"
#         )
#         map_key = f"{source_file}-{page}-{raw_context_snippet}-{data_type}"
#         if map_key in session_state.global_citation_details_map:
#             return session_state.global_citation_details_map[map_key], citation_detail_html
#         else:
#             citation_number = len(session_state.global_citation_details_list) + 1
#             session_state.global_citation_details_list.append((citation_number, citation_detail_html))
#             session_state.global_citation_details_map[map_key] = citation_number
#             session_state.global_references.add(f"[{citation_number}] Source: {source_file}, Page: {page}, Type: {data_type.capitalize()}, Context: {raw_context_snippet}")
#             return citation_number, citation_detail_html

#     def extract_numbers_and_phrases(text):
#         numbers = re.findall(
#             r'\d+\.?\d*%\s*(?:Y/Y|year-on-year)?|€?\d+\.?\d*\s*(?:million|billion|thousand)?|\$\d+\.?\d*\s*(?:million|billion|thousand)?',
#             text, re.IGNORECASE
#         )
#         key_phrases = re.findall(r'\b(?:revenue|EBIT|adjusted EBIT|margin|outlook|growth|segment|solution|service|employees|listed|geographically|headquartered|acquisition|partnership|strategy|base|installation|modernization)\b', text, re.IGNORECASE)
#         return numbers, key_phrases

#     def validate_citation(sentence, snippet, sentence_numbers, sentence_phrases):
#         return True  # Aggressive citation as per preference

#     insertions = []
#     cited_original_spans = []
#     doc_snippets = []
#     doc_metadata = []
#     file_hash = "|".join(session_state.processed_file_hashes)
#     cache_key = f"snippets_{file_hash}"
#     if cache_key in session_state.cache:
#         doc_snippets, doc_metadata, doc_embeddings = session_state.cache[cache_key]
#     else:
#         if source_documents:
#             for doc in source_documents:
#                 content = doc.page_content.replace("\n", " ").strip()
#                 chunk_size_for_embedding = 500
#                 chunk_overlap_for_embedding = 100
#                 for i in range(0, len(content), chunk_size_for_embedding - chunk_overlap_for_embedding):
#                     snippet = content[i:i + chunk_size_for_embedding]
#                     if snippet.strip():
#                         doc_snippets.append(snippet)
#                         doc_metadata.append((doc.metadata['source'], doc.metadata['page'], doc.metadata.get('type', 'text')))
#         if doc_snippets:
#             doc_embeddings = sentence_model.encode(doc_snippets, convert_to_tensor=True, show_progress_bar=False)
#             session_state.cache[cache_key] = (doc_snippets, doc_metadata, doc_embeddings)
#         else:
#             return text

#     if not doc_snippets:
#         return text

#     sentences = sent_tokenize(text)
#     sentence_positions = []
#     current_pos = 0
#     for sentence_raw in sentences:
#         if not sentence_raw.strip():
#             current_pos += len(sentence_raw)
#             continue
#         sentence_start = text.find(sentence_raw, current_pos)
#         if sentence_start == -1:
#             sentence_start = current_pos
#         sentence_end = sentence_start + len(sentence_raw)
#         sentence_positions.append((sentence_raw, sentence_start, sentence_end))
#         current_pos = sentence_end

#     for sentence_raw, start_pos_s, end_pos_s in sentence_positions:
#         already_cited = False
#         for cited_start, cited_end in cited_original_spans:
#             if max(start_pos_s, cited_start) < min(end_pos_s, cited_end):
#                 already_cited = True
#                 break
#         if already_cited or not sentence_raw.strip():
#             continue

#         sentence_embedding = sentence_model.encode(sentence_raw, convert_to_tensor=True)
#         scores = util.cos_sim(sentence_embedding, doc_embeddings).flatten()
#         best_match_index = scores.argmax().item()
#         best_score = scores[best_match_index].item()
        
#         sentence_numbers, sentence_phrases = extract_numbers_and_phrases(sentence_raw)
#         has_keywords = bool(sentence_numbers or sentence_phrases)
        
#         best_snippet = doc_snippets[best_match_index]
#         is_valid_match = validate_citation(sentence_raw, best_snippet, sentence_numbers, sentence_phrases)

#         should_cite = False
#         universal_low_threshold = 0.20
#         if best_score >= universal_low_threshold:
#             should_cite = True

#         if should_cite:
#             source_file, page, data_type = doc_metadata[best_match_index]
#             raw_context = doc_snippets[best_match_index]
#             citation_number, citation_tooltip_html = _get_citation_info(source_file, page, raw_context, data_type)
            
#             citation_html_tag = (
#                 f"<sup><span class='citation' data-source='{html.escape(source_file)}' data-page='{page}' data-context='{html.escape(raw_context)}'>[{citation_number}]"
#                 f"<span class='citation-card'>{citation_tooltip_html}</span></span></sup>"
#             )
            

#             original_sentence_segment = text[start_pos_s:end_pos_s]
#             last_punct_match = re.search(r'([.!?])(\s*)$', original_sentence_segment)
#             if last_punct_match:
#                 insertion_point = last_punct_match.start(1)
#                 modified_segment = (
#                     original_sentence_segment[:insertion_point] +
#                     citation_html_tag +
#                     original_sentence_segment[insertion_point:]
#                 )
#             else:
#                 modified_segment = original_sentence_segment + citation_html_tag
            
#             insertions.append((start_pos_s, modified_segment, end_pos_s))
#             cited_original_spans.append((start_pos_s, end_pos_s))

#     insertions.sort(key=lambda x: x[0], reverse=True)
#     final_text = text
#     for start_idx, new_content, end_idx in insertions:
#         final_text = final_text[:start_idx] + new_content + final_text[end_idx:]
#     return final_text

# def clean_company_name(name):
#     """
#     Cleans the company name for use in filenames.
#     Args:
#         name: Company name string.
#     Returns:
#         Cleaned company name.
#     """
#     if not isinstance(name, str):
#         return DEFAULT_COMPANY_NAME
#     cleaned_name = name.replace('\n', '').replace('\r', '').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace(' ', '_').strip()
#     return cleaned_name

# def get_company_name_from_llm(llm, raw_text, file_names):
#     """
#     Uses an LLM to extract the company's full name from the raw text.
#     Args:
#         llm: Language model instance.
#         raw_text: Concatenated text from documents.
#         file_names: List of file names.
#     Returns:
#         Company name or DEFAULT_COMPANY_NAME if not found.
#     """
#     if not raw_text.strip():
#         return DEFAULT_COMPANY_NAME
    
#     text_sample = raw_text[:min(len(raw_text), 4000)]
#     file_names_str = ", ".join(file_names)

#     prompt = PromptTemplate.from_template(
#         f"""
#         Extract the full and correct company name from the following text and associated filenames.
#         Prioritize the official company name as it appears prominently in the initial pages of a report, or in titles.
#         Look for formal names, often followed by suffixes like "AG", "Group", "Corp.", "Inc.", "Ltd.", "Oyj", "Plc", "NV", "AB", "SE", etc.
        
#         **CRUCIALLY, DO NOT return generic document titles or report types as the company name, even if they are capitalized or appear to be names.**
#         Explicitly ignore and filter out these terms if they appear alone or as the primary extracted name:
#         "Annual Report", "Quarterly Report", "Earnings Call", "Presentation", "Transcript", "Review", "Statement", "Financials", "Update Call", "Q1", "Q4", "Combined Management Report".
        
#         If no clear company name is found after these considerations, or if the extracted name is one of the generic terms, return "{DEFAULT_COMPANY_NAME}".

#         Text Sample:
#         {text_sample}

#         Associated File Names:
#         {file_names_str}

#         Company Name:
#         """
#     )
#     chain = prompt | llm | StrOutputParser()

#     try:
#         time.sleep(2)
#         company_name = chain.invoke({"text": text_sample, "file_names": file_names_str}).strip()
        
#         false_positives = [
#             "annual report", "quarterly report", "earnings call", "presentation", "transcript", 
#             "review", "statement", "financials", "update call", "q1", "q4", "combined management report",
#             "group", "ag", "inc", "ltd", "corp", "plc", "nv", "ab", "se", "oyj"
#         ]
        
#         if company_name == DEFAULT_COMPANY_NAME or not company_name or len(company_name) < 3:
#             return DEFAULT_COMPANY_NAME

#         if any(company_name.lower() == fp for fp in false_positives):
#             return DEFAULT_COMPANY_NAME

#         cleaned_name = re.sub(r'(?i)\s*(?:Inc|Ltd|Corp|Oyj|AG|SE|GmbH|Pty Ltd|Plc|NV|AB|Group)\s*$', '', company_name).strip()
#         if cleaned_name and len(cleaned_name) >= 3 and not any(cleaned_name.lower() == fp for fp in false_positives):
#             return clean_company_name(cleaned_name)
        
#         if any(company_name.lower() == fp for fp in false_positives):
#             return DEFAULT_COMPANY_NAME

#         return clean_company_name(company_name)

#     except Exception as e:
#         return DEFAULT_COMPANY_NAME, f"Could not extract company name using LLM: {e}"

# def extract_company_name_fallback_regex(text, file_names):
#     """
#     Fallback method to extract company name using regex.
#     Args:
#         text: Raw text from documents.
#         file_names: List of file names.
#     Returns:
#         Company name or DEFAULT_COMPANY_NAME if not found.
#     """
#     if not text or not isinstance(text, str):
#         return DEFAULT_COMPANY_NAME

#     text_sample = text[:min(len(text), 4000)]

#     corporate_suffixes = [
#         r'Corp\.?', r'Inc\.?', r'Ltd\.?', r'Pty Ltd', r'GmbH', r'AG', r'SE', r'SA',
#         r'Co\.?', r'Group', r'Holding', r'Industries', r'Solutions', r'Systems',
#         r'Technologies', r'Oyj', r'Plc', r'NV', r'AB'
#     ]
    
#     company_name_pattern_with_suffix = r"([A-Z][A-Za-z0-9\s&\.-]+(?: " + "| ".join(corporate_suffixes) + r")(?!\s*(?:Annual Report|Q\d{1,2}|Earnings Call|Interim Report|Presentation|Transcript|Review|Statement|Financials|Update Call)))"
    
#     match = re.search(company_name_pattern_with_suffix, text_sample, re.IGNORECASE)
#     if match:
#         return clean_company_name(match.group(1))

#     for file_name in file_names:
#         file_name_match = re.search(r"([A-Z][A-Za-z\s&\.-]+)(?:_Annual Review|_Q\d{1,2}|_Earnings Call|_Interim Report|_Presentation|_Transcript|_Update Call)?(?:_|\s|\.)*(?:Annual|Quarterly|Report|Statement|Presentation|Review|Call|FY|Q\d|Transcript)?(?:\.pdf)?", file_name, re.IGNORECASE)
#         if file_name_match:
#             extracted_name = file_name_match.group(1).replace("_", " ").strip()
#             false_positives_in_filename = [
#                 'corrected', 'transcript', 'q1', 'q4', 'review', 'earnings', 'call', 'interim', 
#                 'presentation', 'annual report', 'quarterly report', 'statement', 'financials', 
#                 'powerpoint-präsentation', 'update call', 'annual review', 'group'
#             ]
#             if len(extracted_name) > 2 and not any(fp in extracted_name.lower() for fp in false_positives_in_filename):
#                 if 'group' in extracted_name.lower() and extracted_name.lower().endswith('group'):
#                     return clean_company_name(extracted_name.replace("Group", "").replace("group", "").strip())
#                 return clean_company_name(extracted_name)

#     general_company_pattern = re.compile(
#         r'\b([A-Z][A-Za-z0-9\s&\.-]+(?: ' + '| '.join(corporate_suffixes) + r')?)\b'
#     )
    
#     matches = general_company_pattern.findall(text_sample)
    
#     if matches:
#         false_positives = [
#             'services', 'solutions', 'systems', 'technologies', 'company', 'corporation', 'financial', 
#             'report', 'annual', 'quarterly', 'flow', 'people', 'corrected', 'transcript', 'update', 
#             'thesis', 'business', 'overview', 'earnings', 'investment', 'q1', 'q4', 'review', 'call', 
#             'interim', 'presentation', 'statement', 'financials', 'management', 'kion', 'group', 'ag',
#             'dax', 'mdax', 'outlook', 'key figures'
#         ]
        
#         matches.sort(key=len, reverse=True)

#         for match in matches:
#             clean_match = match.strip(' .,;:')
#             words = clean_match.lower().split()
            
#             if len(clean_match) < 3 or any(clean_match.lower() == fp for fp in false_positives):
#                 continue
            
#             if all(word in false_positives for word in words) and len(words) > 1:
#                 continue

#             if any(re.search(suffix.strip(r'\b'), clean_match, re.IGNORECASE) for suffix in corporate_suffixes):
#                 name_before_suffix = re.sub(r'(?i)\s*(?:' + '|'.join(corporate_suffixes) + r')$', '', clean_match).strip()
#                 if not name_before_suffix or any(name_before_suffix.lower() == fp for fp in false_positives):
#                     continue
#                 return clean_company_name(clean_match)
            
#             if not any(phrase in clean_match.lower() for phrase in ['business overview', 'quarterly earnings', 'investment thesis', 'annual report', 'quarterly report', 'statement', 'financials', 'key figures', 'overview', 'highlights']):
#                 if len(words) >= 1 and all(word.istitle() or word.isupper() for word in words):
#                     return clean_company_name(clean_match)

#     return DEFAULT_COMPANY_NAME

# def _draw_page_and_footer(canvas_obj, doc_obj, company_name, header_style, footer_style):
#     """
#     Helper function to draw headers and footers on each page of the PDF.
#     Args:
#         canvas_obj: ReportLab canvas object.
#         doc_obj: ReportLab document object.
#         company_name: Name of the company.
#         header_style: ParagraphStyle for header.
#         footer_style: ParagraphStyle for footer.
#     """
#     canvas_obj.saveState()
#     page_num = canvas_obj.getPageNumber()
    
#     current_time_for_pdf = datetime.now().strftime("%Y-%m-%d")
#     footer_text = f"Page {page_num} | Generated on {current_time_for_pdf}"
#     footer_paragraph = Paragraph(footer_text, footer_style)
#     footer_width = doc_obj.width
#     footer_height = footer_paragraph.wrap(footer_width, doc_obj.bottomMargin)[1]
#     footer_x_position = doc_obj.leftMargin
#     footer_y_position = 0.5 * inch
#     footer_paragraph.drawOn(canvas_obj, footer_x_position, footer_y_position)

#     canvas_obj.restoreState()

# def generate_styled_pdf(company_name, business_overview_text, quarterly_highlights_text, investment_thesis_text):
#     """
#     Generates a styled PDF report from the provided text sections.
#     Args:
#         company_name: Name of the company.
#         business_overview_text: Business overview text.
#         quarterly_highlights_text: Quarterly earnings text.
#         investment_thesis_text: Investment thesis text.
#         references: List of reference strings.
#     Returns:
#         Tuple: (BytesIO buffer containing PDF, error message if any).
#     """
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4,
#                             rightMargin=inch, leftMargin=inch,
#                             topMargin=0.75 * inch, bottomMargin=inch)
    
#     styles = getSampleStyleSheet()
#     if 'CompanyNameCentered' not in styles:
#         styles.add(ParagraphStyle(name='CompanyNameCentered', fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=0.10 * inch))
#     if 'Heading' not in styles:
#         styles.add(ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, leading=18, spaceBefore=0.15 * inch, spaceAfter=0.06 * inch, alignment=TA_LEFT))
#     if 'BodyText' not in styles:
#         styles.add(ParagraphStyle(name='BodyText', fontName='Helvetica', fontSize=10, leading=12, alignment=TA_JUSTIFY, spaceAfter=0.03 * inch))
#     if 'References' not in styles:
#         styles.add(ParagraphStyle(name='References', fontName='Helvetica', fontSize=8, leading=10, spaceBefore=0.1 * inch))
#     if 'Footer' not in styles:
#         styles.add(ParagraphStyle(name='Footer', fontName='Helvetica-Oblique', fontSize=8, alignment=TA_CENTER))
#     if 'PageHeader' not in styles:
#         styles.add(ParagraphStyle(name='PageHeader', fontName='Helvetica-Bold', fontSize=12, leading=14, alignment=TA_CENTER))

#     story = []
#     width, height = A4

#     # Apply unit conversion to all sections before PDF generation
#     conversion_type = session_state.cache.get('selected_unit_conversion', 'None')
#     custom_mappings = {
#         "%": session_state.cache.get('unit_%', 'percentage'),
#         "~": session_state.cache.get('unit_~', 'approximately'),
#         "$": session_state.cache.get('unit_$', 'US dollar'),
#         "(Y/Y)": session_state.cache.get('unit_(Y/Y)', 'year-on-year'),
#         "€": session_state.cache.get('unit_€', 'Euro'),
#         "million": session_state.cache.get('unit_million', 'M'),
#         "<": session_state.cache.get('unit_<', 'less than'),
#         ">": session_state.cache.get('unit_>', 'greater than')
#     }
#     pdf_business_overview = convert_units(business_overview_text, conversion_type, custom_mappings) if business_overview_text else ""
#     pdf_quarterly_highlights = convert_units(quarterly_highlights_text, conversion_type, custom_mappings) if quarterly_highlights_text else ""
#     pdf_investment_thesis = convert_units(investment_thesis_text, conversion_type, custom_mappings) if investment_thesis_text else ""

#     story.append(Paragraph(company_name if company_name else "Company Analysis Report", styles['CompanyNameCentered']))
#     story.append(Spacer(1, 0.05 * inch))

#     if pdf_business_overview and "Error" not in pdf_business_overview and "Could not" not in pdf_business_overview and "not generate" not in pdf_business_overview:
#         story.append(Paragraph("Business Overview", styles['Heading']))
#         cleaned_text = clean_html_for_pdf(pdf_business_overview)
#         story.append(Paragraph(cleaned_text.replace("\n", "<br/>"), styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))
#     else:
#         story.append(Paragraph("Business Overview", styles['Heading']))
#         story.append(Paragraph("*(Business overview could not be generated from the provided documents.)*", styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))

#     if pdf_quarterly_highlights and "Error" not in pdf_quarterly_highlights and "Could not" not in pdf_quarterly_highlights and "not generate" not in pdf_quarterly_highlights:
#         period_match = re.search(r"(Q\d{1,2}-\d{2}|Q\d{1,2} \d{4}|Fiscal Year \d{4}|\d{4} Fiscal Year|Annual Report \d{4}|quarter ending \w+ \d{1,2}, \d{4}|H\d \d{4} Interim Report)", pdf_quarterly_highlights, re.IGNORECASE)
#         if period_match:
#             quarter_title = period_match.group(0).replace("Q", "Q").replace("-", " ")
#             story.append(Paragraph(f"Quarterly earnings update ({quarter_title})", styles['Heading']))
#         else:
#             story.append(Paragraph("Quarterly earnings update", styles['Heading']))
#         cleaned_text = clean_html_for_pdf(pdf_quarterly_highlights)
#         story.append(Paragraph(cleaned_text.replace("\n", "<br/>"), styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))
#     else:
#         story.append(Paragraph("Quarterly earnings update", styles['Heading']))
#         story.append(Paragraph("*(Quarterly/Annual Earnings Update could not be generated from the provided documents.)*", styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))

#     if pdf_investment_thesis and "Error" not in pdf_investment_thesis and "Could not" not in pdf_investment_thesis and "not generate" not in pdf_investment_thesis:
#         story.append(Paragraph("Investment Thesis", styles['Heading']))
#         cleaned_text = clean_html_for_pdf(pdf_investment_thesis)
#         formatted_thesis = cleaned_text.replace("\n\n", "<br/><br/>").replace("\n", " ")
#         story.append(Paragraph(formatted_thesis, styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))
#     else:
#         story.append(Paragraph("Investment Thesis", styles['Heading']))
#         story.append(Paragraph("*(Investment Thesis could not be generated from the provided documents.)*", styles['BodyText']))
#         story.append(Spacer(1, 0.03 * inch))

#     try:
#         doc.build(story, 
#                   onFirstPage=lambda canvas, doc: _draw_page_and_footer(canvas, doc, company_name, styles['PageHeader'], styles['Footer']),
#                   onLaterPages=lambda canvas, doc: _draw_page_and_footer(canvas, doc, company_name, styles['PageHeader'], styles['Footer']))
#     except Exception as e:
#         return None, f"Error building PDF document: {str(e)}"

#     buffer.seek(0)
#     return buffer, None


# # def modify_report_section(vectordb, user_prompt, section_to_modify, company_name, num_docs, current_section_content):
# #     """
# #     Modifies a specific section of the report based on user prompt, with inline citations.
# #     Args:
# #         vectordb: FAISS vector store.
# #         user_prompt: User's modification prompt.
# #         section_to_modify: Section to modify ('Business Overview', 'Quarterly Earnings', 'Investment Thesis').
# #         company_name: Name of the company.
# #         num_docs: Number of documents in vector store.
# #         current_section_content: Current content of the section.
# #     Returns:
# #         Tuple: (modified text with citations, source documents, error message if any).
# #     """
# #     if not vectordb:
# #         return None, [], "No vector store available to process the modification."

   

# #     llm = ChatGoogleGenerativeAI(
# #         model="gemini-2.5-flash",
# #         google_api_key=os.getenv("GOOGLE_API_KEY"),
# #         temperature=0.0,
# #     )

# #     k_value = min(50, num_docs) if num_docs > 0 else 1
# #     base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
# #     retriever_docs = base_retriever.invoke(user_prompt)

# #     # Select the right prompt
# #     prompt_template = None
# #     if section_to_modify.lower() in ["business overview", "overview"]:
# #         prompt_template = get_business_overview_prompt_template()
# #     elif section_to_modify.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
# #         prompt_template = get_quarterly_earnings_prompt_template()
# #     elif section_to_modify.lower() in ["investment thesis", "thesis"]:
# #         prompt_template = get_investment_thesis_prompt_template()
# #     else:
# #         return None, [], "Invalid section specified."

# #     document_combining_chain = create_stuff_documents_chain(llm, prompt_template)
# #     rag_chain = (
# #         RunnableParallel(
# #             {"context": lambda x: retriever_docs, "input": RunnablePassthrough()}
# #         )
# #         | RunnableParallel(
# #             {"answer": document_combining_chain, "source_documents": lambda x: retriever_docs}
# #         )
# #     )

# #     try:
# #         response = rag_chain.invoke({
# #             "input": user_prompt,
# #             "current_section_content": current_section_content,
# #             "company_name": company_name,
# #             "user_prompt": user_prompt
# #         })
# #         modified_text = response["answer"].strip()
# #         source_docs = response.get("source_documents", [])

# #         if not modified_text or (len(modified_text) < 50 and "remove" not in user_prompt.lower()) or \
# #            any(keyword in modified_text.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
# #             return modified_text, source_docs, "LLM indicated key data might be missing."

        
# #         annotated_text = add_inline_citations(modified_text, source_docs)
# #         return annotated_text, source_docs, None

# #     except Exception as e:
# #         error_msg = f"Error modifying {section_to_modify}: {str(e)}"
# #         if "quota" in str(e).lower():
# #             error_msg += " API quota exceeded."
# #         return None, [], error_msg
# def modify_report_section(
#     vectordb, user_prompt, section_to_modify, company_name, num_docs, current_section_content
# ) -> Tuple[str, list, Optional[str]]:
#     """
#     Modifies a specific section of the report if the requested information is present in the PDFs.
#     Returns (modified_text, source_documents, error_message)
#     """
#     if not vectordb:
#         return None, [], "Vector store is not initialized."

#     try:
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=os.getenv("GOOGLE_API_KEY"),
#             temperature=0.0,
#         )

#         # 1️⃣ Search vectorstore to check if user_prompt data is present
#         retriever = vectordb.as_retriever(search_kwargs={"k": 10})
#         search_results = retriever.invoke(user_prompt)

#         if not search_results or len(search_results) == 0:
#             # 🚨 No relevant data found in PDFs
#             warning = (
#                 "The requested change could not be applied because "
#                 "this information was not found in the uploaded documents."
#             )
#             return current_section_content, [], warning

#         # 2️⃣ If relevant data found, proceed to modify
#         if section_to_modify.lower() in ["business overview", "overview"]:
#             prompt_template = get_business_overview_prompt_template()
#         elif section_to_modify.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
#             prompt_template = get_quarterly_earnings_prompt_template()
#         elif section_to_modify.lower() in ["investment thesis", "thesis"]:
#             prompt_template = get_investment_thesis_prompt_template()
#         else:
#             return None, [], f"Unknown section: {section_to_modify}"

#         document_chain = create_stuff_documents_chain(llm, prompt_template)
#         rag_chain = {
#             "context": lambda _: search_results,
#             "user_prompt": RunnablePassthrough(),
#         } | document_chain

#         modified_text = rag_chain.invoke(user_prompt)
#         modified_text_with_citations = add_inline_citations(modified_text, search_results)

#         return modified_text_with_citations, search_results, None

#     except Exception as e:
#         return None, [], f"Error modifying report: {str(e)}"

# def validate_and_rerun_quarterly_earnings(vectordb, company_name, initial_response, num_docs):
#     """
#     Validates the quarterly earnings response and re-runs if key metrics are missing.
#     Args:
#         vectordb: FAISS vector store.
#         company_name: Name of the company.
#         initial_response: Initial quarterly earnings text.
#         num_docs: Number of documents in vector store.
#     Returns:
#         Tuple: (annotated text, source documents, error message if any).
#     """
#     if not initial_response or len(initial_response) < 50:
#         return initial_response, [], "Quarterly Earnings response invalid or too short."

#     required_metrics = ["revenue", "ebit", "adjusted ebit", "y/y change", "margin", "outlook"]
#     missing_metrics = [metric for metric in required_metrics if metric.lower() not in initial_response.lower()]

#     if missing_metrics:
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=GOOGLE_API_KEY,
#             temperature=0.0,
#         )
#         k_value = min(50, num_docs) if num_docs > 0 else 1
#         cache_key = f"retriever_quarterly_earnings_{company_name}_{'|'.join(session_state.processed_file_hashes)}"
#         if cache_key in session_state.cache:
#             retriever_docs = session_state.cache[cache_key]
#         else:
#             base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
#             retriever_docs = base_retriever.invoke(
#                 f"For {company_name}, ensure the summary compares Q1 2025 with Q1 2024, includes total revenue, EBIT, adjusted EBIT, margin with y/y change, segment-specific revenue, EBIT, adjusted EBIT, and full-year 2025 outlook if available in the Q1 2025 Quarterly Statement or Annual Report. Exclude sales, free cash flow, and order intake data."
#             )
#             session_state.cache[cache_key] = retriever_docs

#         document_combining_chain = create_stuff_documents_chain(llm, get_quarterly_earnings_prompt_template())
#         rag_chain = (
#             RunnableParallel(
#                 {"context": lambda x: retriever_docs, "input": RunnablePassthrough()}
#             )
#             | RunnableParallel(
#                 {"answer": document_combining_chain, "source_documents": lambda x: retriever_docs}
#             )
#         )

#         try:
#             response = rag_chain.invoke({"input": f"For {company_name}, ensure the summary compares Q1 2025 with Q1 2024, includes total revenue, EBIT, adjusted EBIT, margin with y/y change, segment-specific revenue, EBIT, adjusted EBIT, and full-year 2025 outlook if available in the Q1 2025 Quarterly Statement or Annual Report. Exclude sales, free cash flow, and order intake data."})
#             modified_text = response["answer"].strip()
#             source_docs = response.get("source_documents", [])
#             annotated_text = add_inline_citations(modified_text, source_docs)
#             return annotated_text, source_docs, None
#         except Exception as e:
#             error_msg = f"Error during re-run: {str(e)}"
#             if "quota" in str(e).lower():
#                 error_msg += " API quota exceeded."
#             return initial_response, [], error_msg

#     cache_key = f"retriever_quarterly_earnings_initial_{company_name}_{'|'.join(session_state.processed_file_hashes)}"
#     if cache_key in session_state.cache:
#         initial_sources = session_state.cache[cache_key]
#     else:
#         initial_sources = vectordb.as_retriever(search_kwargs={"k": k_value}).invoke(initial_response)
#         session_state.cache[cache_key] = initial_sources

#     annotated_text = add_inline_citations(initial_response, initial_sources)
#     return annotated_text, initial_sources, None


# # def extract_key_thesis_points(vectordb, num_docs):
# #     """
# #     Extract key investment thesis points as bullet points or short sentences.
# #     """
# #     try:
# #         if not vectordb or num_docs == 0:
# #             return [], "No documents available to extract thesis points."

# #         llm = ChatGoogleGenerativeAI(
# #             model="gemini-2.5-flash",
# #             google_api_key=os.getenv("GOOGLE_API_KEY"),
# #             temperature=0.2
# #         )

# #         retriever =MultiQueryRetriever.from_llm (retriever=vectordb.as_retriever(search_kwargs={"k": min(50, num_docs)} if num_docs > 0 else 1) , llm=llm) 

# #         chain = create_stuff_documents_chain(llm, get_investment_thesis_prompt_template())

# #         rag_chain = (
# #             RunnableParallel({"context": lambda x: retriever.invoke("Summarize investment thesis"), "input": RunnablePassthrough()})
# #             | RunnableParallel({"answer": chain, "source_documents": lambda x: retriever.invoke("Summarize investment thesis")})
# #         )

# #         response = rag_chain.invoke({
# #             "input": "Extract unique and important investment points from the provided documents, distinct from a typical 3-paragraph thesis."
# #         })

# #         text = response.get("answer", "")
# #         source_documents = response.get("source_documents", [])

# #         # 🟨 Optional cleanup: parse text into points
# #         points = [line.strip("-• \n") for line in text.split("\n") if line.strip()]
# #         if not points or all(len(p.strip()) < 5 for p in points):
# #             return [], "No clear thesis points extracted."

# #         return points, None
# #     except Exception as e:
# #         return [], f"Error extracting key thesis points: {str(e)}"
# def extract_key_thesis_points(vectordb, num_docs):
#     if not vectordb:
#         return [], "VectorDB is missing"

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=GOOGLE_API_KEY,
#         temperature=0.0,
#     )

#     k_value = min(50, num_docs) if num_docs > 0 else 1
#     retriever = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm)

#     prompt = get_key_thesis_points_prompt_template()
#     chain = (
#         {"context": retriever, "question": RunnablePassthrough()} 
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     try:
#         key_points_raw = chain.invoke("Extract unique and important investment points from the provided documents, distinct from a typical 3-paragraph thesis.")
#         key_points = [point.strip().lstrip('- ').strip() for point in key_points_raw.split('\n') if point.strip()]
#         return key_points, None

#     except Exception as e:
#         return [], f"Error extracting key thesis points: {str(e)}"


# # def elaborate_on_thesis_point(vectordb, point_summary, num_docs, word_count):
# #     """
# #     Retrieves detailed information for a specific key thesis point.
# #     Args:
# #         vectordb: FAISS vector store.
# #         point_summary: Summary of the thesis point.
# #         num_docs: Number of documents in vector store.
# #         word_count: Desired word count for the response.
# #     Returns:
# #         Tuple: (detailed text with citations, source documents, error message if any).
# #     """
# #     if not vectordb:
# #         return "No documents analyzed.", [], "No documents analyzed."

# #     llm = ChatGoogleGenerativeAI(
# #         model="gemini-2.5-flash",
# #         google_api_key=GOOGLE_API_KEY,
# #         temperature=0.0,
# #     )

# #     k_value = min(50, num_docs) if num_docs > 0 else 1
# #     cache_key = f"retriever_thesis_point_{point_summary}_{'|'.join(session_state.processed_file_hashes)}"
# #     if cache_key in session_state.cache:
# #         retriever_docs = session_state.cache[cache_key]
# #     else:
# #         base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
# #         retriever_docs = base_retriever.invoke(point_summary)
# #         session_state.cache[cache_key] = retriever_docs

# #     chain = (
# #         RunnableParallel(
# #             {"context": lambda x: retriever_docs, "point_summary": RunnablePassthrough(), "word_count": RunnablePassthrough()}
# #         )
# #         | RunnableParallel(
# #             {"answer": get_detailed_explanation_prompt_template() | llm | StrOutputParser(), "source_documents": lambda x: retriever_docs}
# #         )
# #     )

# #     try:
# #         response = chain.invoke({"point_summary": point_summary, "word_count": word_count})
# #         detail = response["answer"].strip()
# #         sources = response.get("source_documents", [])

# #         if not detail or len(detail) < 20 or any(keyword in detail.lower() for keyword in ["not found", "not available", "insufficient information", "could not generate"]):
# #             return f"Detailed information for '{point_summary}' was not found.", [], "Information not found."

# #         annotated_detail = add_inline_citations(detail, sources)
# #         return annotated_detail, sources, None
# #     except Exception as e:
# #         error_msg = f"Error elaborating on thesis point: {str(e)}"
# #         if "quota" in str(e).lower():
# #             error_msg += " API quota exceeded."
# #         return "An error occurred.", [], error_msg
# def elaborate_on_thesis_point(
#     point_summary: str,
#     word_count: int,
#     vectordb,
#     num_docs: int
# ) -> Tuple[str, list, Optional[str]]:
#     """
#     Elaborate a thesis point using RAG (LLM + vectorstore).
#     Returns (elaborated_text, sources, error)
#     """
#     try:
#         if not GOOGLE_API_KEY:
#             return "", [], "Google API key is missing or invalid."

#         if vectordb is None:
#             return "", [], "Vector store is not initialized."

#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=GOOGLE_API_KEY,
#             temperature=0.0
#         )

#         k_value = min(30, num_docs) if num_docs > 0 else 1
#         retriever = MultiQueryRetriever.from_llm(
#             retriever=vectordb.as_retriever(search_kwargs={"k": k_value}),
#             llm=llm
#         )
#         retrieved_docs = retriever.invoke(point_summary)

#         prompt_template = PromptTemplate.from_template(
#             """
#             You are an equity research analyst. Based ONLY on the context below, elaborate this investment thesis point into a single paragraph (~{word_count} words) in professional style.

#             Thesis Point:
#             {point_summary}

#             Context:
#             {context}

#             Elaborated Thesis Point:
#             """
#         )

#         doc_chain = create_stuff_documents_chain(llm, prompt_template)

#         rag_chain = {
#             "context": lambda _: retrieved_docs,
#             "point_summary": RunnablePassthrough(),
#             "word_count": lambda _: word_count
#         } | doc_chain

#         response = rag_chain.invoke(point_summary)
#         annotated_text = add_inline_citations(response.strip(), retrieved_docs)
#         return annotated_text, retrieved_docs, None

#     except Exception as e:
#         return "", [], f"Error during elaboration: {str(e)}"


# def conversational_retrieval(vectordb, files, query, history):
#     """
#     Retrieve relevant documents for conversational context, filtered by selected files.
#     """
#     # Filter documents based on selected files
#     relevant_docs = [doc for doc in vectordb.docstore._dict.values() if doc.metadata["source"] in files]
#     if not relevant_docs:
#         return []

#     # Use MultiQueryRetriever to handle conversational context
#     retriever = MultiQueryRetriever.from_llm(

#         retriever=vectordb.as_retriever(),

#         llm= ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0.2,
#         #include_original_query=True,

#     ))
#     # Combine history and query for context
#     context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nuser: {query}"
#     results = retriever.get_relevant_documents(context)
#     # Filter results to ensure they match selected files
#     return [doc for doc in results if doc.metadata["source"] in files]

# def format_sources_for_display(source_documents):
#     """
#     Formats a list of Document objects into a readable string of unique sources.
#     Args:
#         source_documents: List of Document objects.
#     Returns:
#         Formatted string of sources.
#     """
#     if not source_documents:
#         return "No direct sources found."

#     unique_sources = {}
#     for doc in source_documents:
#         source = doc.metadata.get("source", "Unknown Document")
#         page = doc.metadata.get("page", None)
#         doc_type = doc.metadata.get("type", "text")
#         key = (source, page, doc_type)
#         if key not in unique_sources:
#             unique_sources[key] = (source, page, doc_type)
    
#     formatted_list = []
#     sorted_unique_sources = sorted(list(unique_sources.values()), key=lambda x: (x[0], x[1], x[2]))

#     for source, page, doc_type in sorted_unique_sources:
#         if page is not None:
#             formatted_list.append(f"{source} (Page: {page}, Type: {doc_type.capitalize()})")
#         else:
#             formatted_list.append(f"{source} (Type: {doc_type.capitalize()})")
            
#     return "\n".join(formatted_list)

# def convert_units(text, conversion_profile, custom_mappings=None):
#     """
#     Converts unit symbols in the text based on the conversion profile.
#     Args:
#         text: Input text to convert.
#         conversion_profile: Conversion profile ('Default', 'Words to Symbols', 'Custom').
#         custom_mappings: Optional custom unit mappings.
#     Returns:
#         Text with converted units.
#     """
#     if not text or not isinstance(text, str):
#         return text

#     citation_placeholders = {}
#     def replace_citation(match):
#         placeholder_id = f"CITATION_PLACEHOLDER_{len(citation_placeholders)}"
#         citation_placeholders[placeholder_id] = match.group(0)
#         return placeholder_id

#     text_with_placeholders = re.sub(r'<sup[^>]*?>.*?</sup>', replace_citation, text)

#     conversion_profiles = {
#         "Default": {
#             "%": "percentage", "~": "approximately", "$": "US dollar", "(Y/Y)": "year-on-year",
#             "€": "Euro", "million": "M", "<": "less than", ">": "greater than"
#         },
#         "Words to Symbols": {
#             "%": "%", "~": "~", "$": "$", "(Y/Y)": "(Y/Y)",
#             "€": "€", "million": "million", "<": "<", ">": ">"
#         },
#         "Custom": custom_mappings if custom_mappings else {}
#     }

#     if conversion_profile not in conversion_profiles:
#         conversion_profile = "Default"
#     current_mappings = conversion_profiles.get(conversion_profile, conversion_profiles["Default"])

#     if not current_mappings or not any(current_mappings.values()):
#         for placeholder, original_citation_html in citation_placeholders.items():
#             text_with_placeholders = text_with_placeholders.replace(placeholder, original_citation_html)
#         return text_with_placeholders

#     modified_text = text_with_placeholders
#     conversion_rules = []

#     for symbol, word in current_mappings.items():
#         if not symbol or not word or not symbol.strip() or not word.strip():
#             continue
#         escaped_symbol = re.escape(symbol)
#         conversion_rules.append((rf"(\d+(?:,\d+)?(?:\.\d+)?)\s*{escaped_symbol}(?![^\s(]*\))", rf"\1 {word}"))
#         conversion_rules.append((rf"\({escaped_symbol}\s*(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:[^\)]+)?\)", rf"(\1 {word})"))
#         conversion_rules.append((rf"\b{escaped_symbol}\s*(\d+(?:,\d+)?(?:\.\d+)?)", rf"{word}\1"))
#         conversion_rules.append((rf"\b{escaped_symbol}\b(?!\s*\d)", word))
#         conversion_rules.append((rf"\b{re.escape(word)}\b(?!\s*{escaped_symbol})", symbol))
#         if symbol == "~":
#             conversion_rules.append((rf"(\d+(?:,\d+)?(?:\.\d+)?)\s*approximately", rf"{symbol}\1"))
#             conversion_rules.append((rf"approximately\s*(\d+(?:,\d+)?(?:\.\d+)?)", rf"{symbol}\1"))

#     conversion_rules.sort(key=lambda x: len(x[0]), reverse=True)
#     for pattern, replacement in conversion_rules:
#         modified_text = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)

#     for placeholder, original_citation_html in citation_placeholders.items():
#         modified_text = modified_text.replace(placeholder, original_citation_html)

#     return modified_text


###################################################################################################################################


import os
from typing import Optional, Tuple
from dotenv import load_dotenv
import re
from datetime import datetime
from io import BytesIO
import html
import torch
import time
import pdfplumber
from sentence_transformers import SentenceTransformer, util
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.schema import Document
from langchain.retrievers import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import nltk

# Placeholder for prompt templates (replace with actual templates)
from prompt_templates import (
    get_business_overview_prompt_template,
    get_detailed_explanation_prompt_template,
    get_investment_thesis_prompt_template,
    get_key_thesis_points_prompt_template,
    get_quarterly_earnings_prompt_template
) 

# Configuration
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEFAULT_COMPANY_NAME = "Company Analysis Report"

# Initialize SentenceTransformer model
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
torch.classes.__path__ = []

# Session state equivalent for citation management and caching
class SessionState:
    def __init__(self):
        self.global_citation_details_list = []
        self.global_citation_details_map = {}
        self.global_references = set()
        self.processed_file_hashes = []
        self.cache = {}

session_state = SessionState()

def extract_text_from_pdfs(uploaded_files):
    """
    Extracts text and tables from uploaded PDF files.
    Args:
        uploaded_files: List of file objects (e.g., from file upload).
    Returns:
        Tuple: (list of Document objects, raw concatenated text, list of file names, error message if any).
    """
    all_docs = []
    file_names = []
    raw_texts = []
    
    for file in uploaded_files:
        file_names.append(file.name)
        try:
            with pdfplumber.open(file) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    # 🔍 Store page text for full PDF rendering later
                    if not hasattr(session_state, "full_pdf_text_map"):
                        session_state.full_pdf_text_map = {}

                    session_state.full_pdf_text_map.setdefault(file.name, {})[page_num + 1] = text

                    tables = page.extract_tables()
                    if text.strip():
                        all_docs.append(Document(
                            page_content=text,
                            metadata={"source": file.name, "page": page_num + 1, "type": "text"}
                        ))
                        raw_texts.append(text)
                    table_text_parts = []
                    for table in tables:
                        for row in table:
                            table_text_parts.append(" | ".join(map(lambda x: str(x) if x is not None else "", row)))
                    table_text = "\n".join(table_text_parts)
                    if table_text.strip():
                        all_docs.append(Document(
                            page_content=table_text,
                            metadata={"source": file.name, "page": page_num + 1, "type": "table"}
                        ))
                        raw_texts.append(table_text)
        except Exception as e:
            return None, None, None, f"Error processing PDF {file.name}: {str(e)}"
    raw_text_for_all_docs = "\n\n".join(raw_texts)
    return all_docs, raw_text_for_all_docs, file_names, None

def create_faiss_vectorstore(documents):
    """
    Creates a FAISS vector store from the provided documents.
    Args:
        documents: List of Document objects.
    Returns:
        Tuple: (FAISS vector store, number of documents, error message if any).
    """
    if not documents:
        return None, 0, "No documents provided to create vector store."
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=1000
    )
    docs_for_vectorstore = splitter.split_documents(documents)
    if not docs_for_vectorstore:
        return None, 0, "Document splitting resulted in no documents."
    num_docs = len(docs_for_vectorstore)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    try:
        vectordb = FAISS.from_documents(docs_for_vectorstore, embeddings)
        return vectordb, num_docs, None
    except Exception as e:
        return None, 0, f"Error creating FAISS vector store: {str(e)}"

def clean_html_for_pdf(text_with_html):
    """
    Removes citation-related HTML tags from the text for PDF generation.
    Args:
        text_with_html: Text containing HTML tags.
    Returns:
        Cleaned text without HTML citation tags.
    """
    cleaned = re.sub(r'<sup[^>]*?>.*?</sup>', '', text_with_html)
    return cleaned

def add_inline_citations(text, source_documents): 
    """
    Adds inline citations to the provided text based on source documents.
    Updates global citation state in session_state.
    Args:
        text: Input text to annotate with citations.
        source_documents: List of Document objects for citation sources.
    Returns:
        Text with inline citation HTML tags.
    """
    nltk.download('punkt', quiet=True)
    from nltk.tokenize import sent_tokenize

    def _get_citation_info(source_file, page, raw_context_snippet, data_type):
        display_context_escaped = html.escape(raw_context_snippet)
        if len(display_context_escaped) > 250:
            display_context_escaped = display_context_escaped[:250] + "..."
        citation_detail_html = (
            f"<div class='citation-field'><strong>Source:</strong> {html.escape(source_file)}</div>"
            f"<div class='citation-field'><strong>Page:</strong> {html.escape(str(page))}</div>"
            f"<div class='citation-field'><strong>Type:</strong> {html.escape(data_type.capitalize())}</div>"
            f"<div class='citation-field'><strong>Context:</strong> {display_context_escaped}</div>"
        )
        map_key = f"{source_file}-{page}-{raw_context_snippet}-{data_type}"
        if map_key in session_state.global_citation_details_map:
            return session_state.global_citation_details_map[map_key], citation_detail_html
        else:
            citation_number = len(session_state.global_citation_details_list) + 1
            session_state.global_citation_details_list.append((citation_number, citation_detail_html))
            session_state.global_citation_details_map[map_key] = citation_number
            session_state.global_references.add(f"[{citation_number}] Source: {source_file}, Page: {page}, Type: {data_type.capitalize()}, Context: {raw_context_snippet}")
            return citation_number, citation_detail_html

    def extract_numbers_and_phrases(text):
        numbers = re.findall(
            r'\d+\.?\d*%\s*(?:Y/Y|year-on-year)?|€?\d+\.?\d*\s*(?:million|billion|thousand)?|\$\d+\.?\d*\s*(?:million|billion|thousand)?',
            text, re.IGNORECASE
        )
        key_phrases = re.findall(r'\b(?:revenue|EBIT|adjusted EBIT|margin|outlook|growth|segment|solution|service|employees|listed|geographically|headquartered|acquisition|partnership|strategy|base|installation|modernization)\b', text, re.IGNORECASE)
        return numbers, key_phrases

    def validate_citation(sentence, snippet, sentence_numbers, sentence_phrases):
        return True  # Aggressive citation as per preference

    insertions = []
    cited_original_spans = []
    doc_snippets = []
    doc_metadata = []
    file_hash = "|".join(session_state.processed_file_hashes)
    cache_key = f"snippets_{file_hash}"
    if cache_key in session_state.cache:
        doc_snippets, doc_metadata, doc_embeddings = session_state.cache[cache_key]
    else:
        if source_documents:
            for doc in source_documents:
                content = doc.page_content.replace("\n", " ").strip()
                chunk_size_for_embedding = 500
                chunk_overlap_for_embedding = 100
                for i in range(0, len(content), chunk_size_for_embedding - chunk_overlap_for_embedding):
                    snippet = content[i:i + chunk_size_for_embedding]
                    if snippet.strip():
                        doc_snippets.append(snippet)
                        doc_metadata.append((doc.metadata['source'], doc.metadata['page'], doc.metadata.get('type', 'text')))
        if doc_snippets:
            doc_embeddings = sentence_model.encode(doc_snippets, convert_to_tensor=True, show_progress_bar=False)
            session_state.cache[cache_key] = (doc_snippets, doc_metadata, doc_embeddings)
        else:
            return text

    if not doc_snippets:
        return text

    sentences = sent_tokenize(text)
    sentence_positions = []
    current_pos = 0
    for sentence_raw in sentences:
        if not sentence_raw.strip():
            current_pos += len(sentence_raw)
            continue
        sentence_start = text.find(sentence_raw, current_pos)
        if sentence_start == -1:
            sentence_start = current_pos
        sentence_end = sentence_start + len(sentence_raw)
        sentence_positions.append((sentence_raw, sentence_start, sentence_end))
        current_pos = sentence_end

    for sentence_raw, start_pos_s, end_pos_s in sentence_positions:
        already_cited = False
        for cited_start, cited_end in cited_original_spans:
            if max(start_pos_s, cited_start) < min(end_pos_s, cited_end):
                already_cited = True
                break
        if already_cited or not sentence_raw.strip():
            continue

        sentence_embedding = sentence_model.encode(sentence_raw, convert_to_tensor=True)
        scores = util.cos_sim(sentence_embedding, doc_embeddings).flatten()
        best_match_index = scores.argmax().item()
        best_score = scores[best_match_index].item()
        
        sentence_numbers, sentence_phrases = extract_numbers_and_phrases(sentence_raw)
        has_keywords = bool(sentence_numbers or sentence_phrases)
        
        best_snippet = doc_snippets[best_match_index]
        is_valid_match = validate_citation(sentence_raw, best_snippet, sentence_numbers, sentence_phrases)

        should_cite = False
        universal_low_threshold = 0.20
        if best_score >= universal_low_threshold:
            should_cite = True

        if should_cite:
            source_file, page, data_type = doc_metadata[best_match_index]
            raw_context = doc_snippets[best_match_index]
            citation_number, citation_tooltip_html = _get_citation_info(source_file, page, raw_context, data_type)
            
            citation_html_tag = (
                f"<sup><span class='citation' data-source='{html.escape(source_file)}' data-page='{page}' data-context='{html.escape(raw_context)}'>[{citation_number}]"
                f"<span class='citation-card'>{citation_tooltip_html}</span></span></sup>"
            )
            

            original_sentence_segment = text[start_pos_s:end_pos_s]
            last_punct_match = re.search(r'([.!?])(\s*)$', original_sentence_segment)
            if last_punct_match:
                insertion_point = last_punct_match.start(1)
                modified_segment = (
                    original_sentence_segment[:insertion_point] +
                    citation_html_tag +
                    original_sentence_segment[insertion_point:]
                )
            else:
                modified_segment = original_sentence_segment + citation_html_tag
            
            insertions.append((start_pos_s, modified_segment, end_pos_s))
            cited_original_spans.append((start_pos_s, end_pos_s))

    insertions.sort(key=lambda x: x[0], reverse=True)
    final_text = text
    for start_idx, new_content, end_idx in insertions:
        final_text = final_text[:start_idx] + new_content + final_text[end_idx:]
    return final_text

def clean_company_name(name):
    """
    Cleans the company name for use in filenames.
    Args:
        name: Company name string.
    Returns:
        Cleaned company name.
    """
    if not isinstance(name, str):
        return DEFAULT_COMPANY_NAME
    cleaned_name = name.replace('\n', '').replace('\r', '').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace(' ', '_').strip()
    return cleaned_name

def get_company_name_from_llm(llm, raw_text, file_names):
    """
    Uses an LLM to extract the company's full name from the raw text.
    Args:
        llm: Language model instance.
        raw_text: Concatenated text from documents.
        file_names: List of file names.
    Returns:
        Company name or DEFAULT_COMPANY_NAME if not found.
    """
    if not raw_text.strip():
        return DEFAULT_COMPANY_NAME
    
    text_sample = raw_text[:min(len(raw_text), 4000)]
    file_names_str = ", ".join(file_names)

    prompt = PromptTemplate.from_template(
        f"""
        Extract the full and correct company name from the following text and associated filenames.
        Prioritize the official company name as it appears prominently in the initial pages of a report, or in titles.
        Look for formal names, often followed by suffixes like "AG", "Group", "Corp.", "Inc.", "Ltd.", "Oyj", "Plc", "NV", "AB", "SE", etc.
        
        **CRUCIALLY, DO NOT return generic document titles or report types as the company name, even if they are capitalized or appear to be names.**
        Explicitly ignore and filter out these terms if they appear alone or as the primary extracted name:
        "Annual Report", "Quarterly Report", "Earnings Call", "Presentation", "Transcript", "Review", "Statement", "Financials", "Update Call", "Q1", "Q4", "Combined Management Report".
        
        If no clear company name is found after these considerations, or if the extracted name is one of the generic terms, return "{DEFAULT_COMPANY_NAME}".

        Text Sample:
        {text_sample}

        Associated File Names:
        {file_names_str}

        Company Name:
        """
    )
    chain = prompt | llm | StrOutputParser()

    try:
        time.sleep(2)
        company_name = chain.invoke({"text": text_sample, "file_names": file_names_str}).strip()
        
        false_positives = [
            "annual report", "quarterly report", "earnings call", "presentation", "transcript", 
            "review", "statement", "financials", "update call", "q1", "q4", "combined management report",
            "group", "ag", "inc", "ltd", "corp", "plc", "nv", "ab", "se", "oyj"
        ]
        
        if company_name == DEFAULT_COMPANY_NAME or not company_name or len(company_name) < 3:
            return DEFAULT_COMPANY_NAME

        if any(company_name.lower() == fp for fp in false_positives):
            return DEFAULT_COMPANY_NAME

        cleaned_name = re.sub(r'(?i)\s*(?:Inc|Ltd|Corp|Oyj|AG|SE|GmbH|Pty Ltd|Plc|NV|AB|Group)\s*$', '', company_name).strip()
        if cleaned_name and len(cleaned_name) >= 3 and not any(cleaned_name.lower() == fp for fp in false_positives):
            return clean_company_name(cleaned_name)
        
        if any(company_name.lower() == fp for fp in false_positives):
            return DEFAULT_COMPANY_NAME

        return clean_company_name(company_name)

    except Exception as e:
        return DEFAULT_COMPANY_NAME, f"Could not extract company name using LLM: {e}"

def extract_company_name_fallback_regex(text, file_names):
    """
    Fallback method to extract company name using regex.
    Args:
        text: Raw text from documents.
        file_names: List of file names.
    Returns:
        Company name or DEFAULT_COMPANY_NAME if not found.
    """
    if not text or not isinstance(text, str):
        return DEFAULT_COMPANY_NAME

    text_sample = text[:min(len(text), 4000)]

    corporate_suffixes = [
        r'Corp\.?', r'Inc\.?', r'Ltd\.?', r'Pty Ltd', r'GmbH', r'AG', r'SE', r'SA',
        r'Co\.?', r'Group', r'Holding', r'Industries', r'Solutions', r'Systems',
        r'Technologies', r'Oyj', r'Plc', r'NV', r'AB'
    ]
    
    company_name_pattern_with_suffix = r"([A-Z][A-Za-z0-9\s&\.-]+(?: " + "| ".join(corporate_suffixes) + r")(?!\s*(?:Annual Report|Q\d{1,2}|Earnings Call|Interim Report|Presentation|Transcript|Review|Statement|Financials|Update Call)))"
    
    match = re.search(company_name_pattern_with_suffix, text_sample, re.IGNORECASE)
    if match:
        return clean_company_name(match.group(1))

    for file_name in file_names:
        file_name_match = re.search(r"([A-Z][A-Za-z\s&\.-]+)(?:_Annual Review|_Q\d{1,2}|_Earnings Call|_Interim Report|_Presentation|_Transcript|_Update Call)?(?:_|\s|\.)*(?:Annual|Quarterly|Report|Statement|Presentation|Review|Call|FY|Q\d|Transcript)?(?:\.pdf)?", file_name, re.IGNORECASE)
        if file_name_match:
            extracted_name = file_name_match.group(1).replace("_", " ").strip()
            false_positives_in_filename = [
                'corrected', 'transcript', 'q1', 'q4', 'review', 'earnings', 'call', 'interim', 
                'presentation', 'annual report', 'quarterly report', 'statement', 'financials', 
                'powerpoint-präsentation', 'update call', 'annual review', 'group'
            ]
            if len(extracted_name) > 2 and not any(fp in extracted_name.lower() for fp in false_positives_in_filename):
                if 'group' in extracted_name.lower() and extracted_name.lower().endswith('group'):
                    return clean_company_name(extracted_name.replace("Group", "").replace("group", "").strip())
                return clean_company_name(extracted_name)

    general_company_pattern = re.compile(
        r'\b([A-Z][A-Za-z0-9\s&\.-]+(?: ' + '| '.join(corporate_suffixes) + r')?)\b'
    )
    
    matches = general_company_pattern.findall(text_sample)
    
    if matches:
        false_positives = [
            'services', 'solutions', 'systems', 'technologies', 'company', 'corporation', 'financial', 
            'report', 'annual', 'quarterly', 'flow', 'people', 'corrected', 'transcript', 'update', 
            'thesis', 'business', 'overview', 'earnings', 'investment', 'q1', 'q4', 'review', 'call', 
            'interim', 'presentation', 'statement', 'financials', 'management', 'kion', 'group', 'ag',
            'dax', 'mdax', 'outlook', 'key figures'
        ]
        
        matches.sort(key=len, reverse=True)

        for match in matches:
            clean_match = match.strip(' .,;:')
            words = clean_match.lower().split()
            
            if len(clean_match) < 3 or any(clean_match.lower() == fp for fp in false_positives):
                continue
            
            if all(word in false_positives for word in words) and len(words) > 1:
                continue

            if any(re.search(suffix.strip(r'\b'), clean_match, re.IGNORECASE) for suffix in corporate_suffixes):
                name_before_suffix = re.sub(r'(?i)\s*(?:' + '|'.join(corporate_suffixes) + r')$', '', clean_match).strip()
                if not name_before_suffix or any(name_before_suffix.lower() == fp for fp in false_positives):
                    continue
                return clean_company_name(clean_match)
            
            if not any(phrase in clean_match.lower() for phrase in ['business overview', 'quarterly earnings', 'investment thesis', 'annual report', 'quarterly report', 'statement', 'financials', 'key figures', 'overview', 'highlights']):
                if len(words) >= 1 and all(word.istitle() or word.isupper() for word in words):
                    return clean_company_name(clean_match)

    return DEFAULT_COMPANY_NAME

def _draw_page_and_footer(canvas_obj, doc_obj, company_name, header_style, footer_style):
    """
    Helper function to draw headers and footers on each page of the PDF.
    Args:
        canvas_obj: ReportLab canvas object.
        doc_obj: ReportLab document object.
        company_name: Name of the company.
        header_style: ParagraphStyle for header.
        footer_style: ParagraphStyle for footer.
    """
    canvas_obj.saveState()
    page_num = canvas_obj.getPageNumber()
    
    current_time_for_pdf = datetime.now().strftime("%Y-%m-%d")
    footer_text = f"Page {page_num} | Generated on {current_time_for_pdf}"
    footer_paragraph = Paragraph(footer_text, footer_style)
    footer_width = doc_obj.width
    footer_height = footer_paragraph.wrap(footer_width, doc_obj.bottomMargin)[1]
    footer_x_position = doc_obj.leftMargin
    footer_y_position = 0.5 * inch
    footer_paragraph.drawOn(canvas_obj, footer_x_position, footer_y_position)

    canvas_obj.restoreState()

def generate_styled_pdf(company_name, business_overview_text, quarterly_highlights_text, investment_thesis_text):
    """
    Generates a styled PDF report from the provided text sections.
    Args:
        company_name: Name of the company.
        business_overview_text: Business overview text.
        quarterly_highlights_text: Quarterly earnings text.
        investment_thesis_text: Investment thesis text.
        references: List of reference strings.
    Returns:
        Tuple: (BytesIO buffer containing PDF, error message if any).
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=0.75 * inch, bottomMargin=inch)
    
    styles = getSampleStyleSheet()
    if 'CompanyNameCentered' not in styles:
        styles.add(ParagraphStyle(name='CompanyNameCentered', fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=0.10 * inch))
    if 'Heading' not in styles:
        styles.add(ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, leading=18, spaceBefore=0.15 * inch, spaceAfter=0.06 * inch, alignment=TA_LEFT))
    if 'BodyText' not in styles:
        styles.add(ParagraphStyle(name='BodyText', fontName='Helvetica', fontSize=10, leading=12, alignment=TA_JUSTIFY, spaceAfter=0.03 * inch))
    if 'References' not in styles:
        styles.add(ParagraphStyle(name='References', fontName='Helvetica', fontSize=8, leading=10, spaceBefore=0.1 * inch))
    if 'Footer' not in styles:
        styles.add(ParagraphStyle(name='Footer', fontName='Helvetica-Oblique', fontSize=8, alignment=TA_CENTER))
    if 'PageHeader' not in styles:
        styles.add(ParagraphStyle(name='PageHeader', fontName='Helvetica-Bold', fontSize=12, leading=14, alignment=TA_CENTER))

    story = []
    width, height = A4

    # Apply unit conversion to all sections before PDF generation
    conversion_type = session_state.cache.get('selected_unit_conversion', 'None')
    custom_mappings = {
        "%": session_state.cache.get('unit_%', 'percentage'),
        "~": session_state.cache.get('unit_~', 'approximately'),
        "$": session_state.cache.get('unit_$', 'US dollar'),
        "(Y/Y)": session_state.cache.get('unit_(Y/Y)', 'year-on-year'),
        "€": session_state.cache.get('unit_€', 'Euro'),
        "million": session_state.cache.get('unit_million', 'M'),
        "<": session_state.cache.get('unit_<', 'less than'),
        ">": session_state.cache.get('unit_>', 'greater than')
    }
    pdf_business_overview = convert_units(business_overview_text, conversion_type, custom_mappings) if business_overview_text else ""
    pdf_quarterly_highlights = convert_units(quarterly_highlights_text, conversion_type, custom_mappings) if quarterly_highlights_text else ""
    pdf_investment_thesis = convert_units(investment_thesis_text, conversion_type, custom_mappings) if investment_thesis_text else ""

    story.append(Paragraph(company_name if company_name else "Company Analysis Report", styles['CompanyNameCentered']))
    story.append(Spacer(1, 0.05 * inch))

    if pdf_business_overview and "Error" not in pdf_business_overview and "Could not" not in pdf_business_overview and "not generate" not in pdf_business_overview:
        story.append(Paragraph("Business Overview", styles['Heading']))
        cleaned_text = clean_html_for_pdf(pdf_business_overview)
        story.append(Paragraph(cleaned_text.replace("\n", "<br/>"), styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))
    else:
        story.append(Paragraph("Business Overview", styles['Heading']))
        story.append(Paragraph("*(Business overview could not be generated from the provided documents.)*", styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))

    if pdf_quarterly_highlights and "Error" not in pdf_quarterly_highlights and "Could not" not in pdf_quarterly_highlights and "not generate" not in pdf_quarterly_highlights:
        period_match = re.search(r"(Q\d{1,2}-\d{2}|Q\d{1,2} \d{4}|Fiscal Year \d{4}|\d{4} Fiscal Year|Annual Report \d{4}|quarter ending \w+ \d{1,2}, \d{4}|H\d \d{4} Interim Report)", pdf_quarterly_highlights, re.IGNORECASE)
        if period_match:
            quarter_title = period_match.group(0).replace("Q", "Q").replace("-", " ")
            story.append(Paragraph(f"Quarterly earnings update ({quarter_title})", styles['Heading']))
        else:
            story.append(Paragraph("Quarterly earnings update", styles['Heading']))
        cleaned_text = clean_html_for_pdf(pdf_quarterly_highlights)
        story.append(Paragraph(cleaned_text.replace("\n", "<br/>"), styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))
    else:
        story.append(Paragraph("Quarterly earnings update", styles['Heading']))
        story.append(Paragraph("*(Quarterly/Annual Earnings Update could not be generated from the provided documents.)*", styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))

    if pdf_investment_thesis and "Error" not in pdf_investment_thesis and "Could not" not in pdf_investment_thesis and "not generate" not in pdf_investment_thesis:
        story.append(Paragraph("Investment Thesis", styles['Heading']))
        cleaned_text = clean_html_for_pdf(pdf_investment_thesis)
        formatted_thesis = cleaned_text.replace("\n\n", "<br/><br/>").replace("\n", " ")
        story.append(Paragraph(formatted_thesis, styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))
    else:
        story.append(Paragraph("Investment Thesis", styles['Heading']))
        story.append(Paragraph("*(Investment Thesis could not be generated from the provided documents.)*", styles['BodyText']))
        story.append(Spacer(1, 0.03 * inch))

    try:
        doc.build(story, 
                  onFirstPage=lambda canvas, doc: _draw_page_and_footer(canvas, doc, company_name, styles['PageHeader'], styles['Footer']),
                  onLaterPages=lambda canvas, doc: _draw_page_and_footer(canvas, doc, company_name, styles['PageHeader'], styles['Footer']))
    except Exception as e:
        return None, f"Error building PDF document: {str(e)}"

    buffer.seek(0)
    return buffer, None


# def modify_report_section(vectordb, user_prompt, section_to_modify, company_name, num_docs, current_section_content):
#     """
#     Modifies a specific section of the report based on user prompt, with inline citations.
#     Args:
#         vectordb: FAISS vector store.
#         user_prompt: User's modification prompt.
#         section_to_modify: Section to modify ('Business Overview', 'Quarterly Earnings', 'Investment Thesis').
#         company_name: Name of the company.
#         num_docs: Number of documents in vector store.
#         current_section_content: Current content of the section.
#     Returns:
#         Tuple: (modified text with citations, source documents, error message if any).
#     """
#     if not vectordb:
#         return None, [], "No vector store available to process the modification."

   

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0.0,
#     )

#     k_value = min(50, num_docs) if num_docs > 0 else 1
#     base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
#     retriever_docs = base_retriever.invoke(user_prompt)

#     # Select the right prompt
#     prompt_template = None
#     if section_to_modify.lower() in ["business overview", "overview"]:
#         prompt_template = get_business_overview_prompt_template()
#     elif section_to_modify.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
#         prompt_template = get_quarterly_earnings_prompt_template()
#     elif section_to_modify.lower() in ["investment thesis", "thesis"]:
#         prompt_template = get_investment_thesis_prompt_template()
#     else:
#         return None, [], "Invalid section specified."

#     document_combining_chain = create_stuff_documents_chain(llm, prompt_template)
#     rag_chain = (
#         RunnableParallel(
#             {"context": lambda x: retriever_docs, "input": RunnablePassthrough()}
#         )
#         | RunnableParallel(
#             {"answer": document_combining_chain, "source_documents": lambda x: retriever_docs}
#         )
#     )

#     try:
#         response = rag_chain.invoke({
#             "input": user_prompt,
#             "current_section_content": current_section_content,
#             "company_name": company_name,
#             "user_prompt": user_prompt
#         })
#         modified_text = response["answer"].strip()
#         source_docs = response.get("source_documents", [])

#         if not modified_text or (len(modified_text) < 50 and "remove" not in user_prompt.lower()) or \
#            any(keyword in modified_text.lower() for keyword in ["not provided", "not available", "insufficient information", "could not generate"]):
#             return modified_text, source_docs, "LLM indicated key data might be missing."

        
#         annotated_text = add_inline_citations(modified_text, source_docs)
#         return annotated_text, source_docs, None

#     except Exception as e:
#         error_msg = f"Error modifying {section_to_modify}: {str(e)}"
#         if "quota" in str(e).lower():
#             error_msg += " API quota exceeded."
#         return None, [], error_msg
def modify_report_section(
    vectordb, user_prompt, section_to_modify, company_name, num_docs, current_section_content
) -> Tuple[str, list, Optional[str]]:
    """
    Modifies a specific section of the report if the requested information is present in the PDFs.
    Returns (modified_text, source_documents, error_message)
    """
    if not vectordb:
        return None, [], "Vector store is not initialized."

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.0,
        )

        # 1️⃣ Search vectorstore to check if user_prompt data is present
        retriever = vectordb.as_retriever(search_kwargs={"k": 10})
        search_results = retriever.invoke(user_prompt)

        if not search_results or len(search_results) == 0:
            # 🚨 No relevant data found in PDFs
            warning = (
                "The requested change could not be applied because "
                "this information was not found in the uploaded documents."
            )
            return current_section_content, [], warning

        # 2️⃣ If relevant data found, proceed to modify
        if section_to_modify.lower() in ["business overview", "overview"]:
            prompt_template = get_business_overview_prompt_template()
        elif section_to_modify.lower() in ["quarterly earnings", "earnings", "quarterly highlights"]:
            prompt_template = get_quarterly_earnings_prompt_template()
        elif section_to_modify.lower() in ["investment thesis", "thesis"]:
            prompt_template = get_investment_thesis_prompt_template()
        else:
            return None, [], f"Unknown section: {section_to_modify}"

        document_chain = create_stuff_documents_chain(llm, prompt_template)
        rag_chain = {
            "context": lambda _: search_results,
            "user_prompt": RunnablePassthrough(),
        } | document_chain

        modified_text = rag_chain.invoke(user_prompt)
        modified_text_with_citations = add_inline_citations(modified_text, search_results)

        return modified_text_with_citations, search_results, None

    except Exception as e:
        return None, [], f"Error modifying report: {str(e)}"

def validate_and_rerun_quarterly_earnings(vectordb, company_name, initial_response, num_docs):
    """
    Validates the quarterly earnings response and re-runs if key metrics are missing.
    Args:
        vectordb: FAISS vector store.
        company_name: Name of the company.
        initial_response: Initial quarterly earnings text.
        num_docs: Number of documents in vector store.
    Returns:
        Tuple: (annotated text, source documents, error message if any).
    """
    if not initial_response or len(initial_response) < 50:
        return initial_response, [], "Quarterly Earnings response invalid or too short."

    required_metrics = ["revenue", "ebit", "adjusted ebit", "y/y change", "margin", "outlook"]
    missing_metrics = [metric for metric in required_metrics if metric.lower() not in initial_response.lower()]

    if missing_metrics:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.0,
        )
        k_value = min(50, num_docs) if num_docs > 0 else 1
        cache_key = f"retriever_quarterly_earnings_{company_name}_{'|'.join(session_state.processed_file_hashes)}"
        if cache_key in session_state.cache:
            retriever_docs = session_state.cache[cache_key]
        else:
            base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
            retriever_docs = base_retriever.invoke(
                f"For {company_name}, ensure the summary compares Q1 2025 with Q1 2024, includes total revenue, EBIT, adjusted EBIT, margin with y/y change, segment-specific revenue, EBIT, adjusted EBIT, and full-year 2025 outlook if available in the Q1 2025 Quarterly Statement or Annual Report. Exclude sales, free cash flow, and order intake data."
            )
            session_state.cache[cache_key] = retriever_docs

        document_combining_chain = create_stuff_documents_chain(llm, get_quarterly_earnings_prompt_template())
        rag_chain = (
            RunnableParallel(
                {"context": lambda x: retriever_docs, "input": RunnablePassthrough()}
            )
            | RunnableParallel(
                {"answer": document_combining_chain, "source_documents": lambda x: retriever_docs}
            )
        )

        try:
            response = rag_chain.invoke({"input": f"For {company_name}, ensure the summary compares Q1 2025 with Q1 2024, includes total revenue, EBIT, adjusted EBIT, margin with y/y change, segment-specific revenue, EBIT, adjusted EBIT, and full-year 2025 outlook if available in the Q1 2025 Quarterly Statement or Annual Report. Exclude sales, free cash flow, and order intake data."})
            modified_text = response["answer"].strip()
            source_docs = response.get("source_documents", [])
            annotated_text = add_inline_citations(modified_text, source_docs)
            return annotated_text, source_docs, None
        except Exception as e:
            error_msg = f"Error during re-run: {str(e)}"
            if "quota" in str(e).lower():
                error_msg += " API quota exceeded."
            return initial_response, [], error_msg

    cache_key = f"retriever_quarterly_earnings_initial_{company_name}_{'|'.join(session_state.processed_file_hashes)}"
    if cache_key in session_state.cache:
        initial_sources = session_state.cache[cache_key]
    else:
        initial_sources = vectordb.as_retriever(search_kwargs={"k": k_value}).invoke(initial_response)
        session_state.cache[cache_key] = initial_sources

    annotated_text = add_inline_citations(initial_response, initial_sources)
    return annotated_text, initial_sources, None


# def extract_key_thesis_points(vectordb, num_docs):
#     """
#     Extract key investment thesis points as bullet points or short sentences.
#     """
#     try:
#         if not vectordb or num_docs == 0:
#             return [], "No documents available to extract thesis points."

#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=os.getenv("GOOGLE_API_KEY"),
#             temperature=0.2
#         )

#         retriever =MultiQueryRetriever.from_llm (retriever=vectordb.as_retriever(search_kwargs={"k": min(50, num_docs)} if num_docs > 0 else 1) , llm=llm) 

#         chain = create_stuff_documents_chain(llm, get_investment_thesis_prompt_template())

#         rag_chain = (
#             RunnableParallel({"context": lambda x: retriever.invoke("Summarize investment thesis"), "input": RunnablePassthrough()})
#             | RunnableParallel({"answer": chain, "source_documents": lambda x: retriever.invoke("Summarize investment thesis")})
#         )

#         response = rag_chain.invoke({
#             "input": "Extract unique and important investment points from the provided documents, distinct from a typical 3-paragraph thesis."
#         })

#         text = response.get("answer", "")
#         source_documents = response.get("source_documents", [])

#         # 🟨 Optional cleanup: parse text into points
#         points = [line.strip("-• \n") for line in text.split("\n") if line.strip()]
#         if not points or all(len(p.strip()) < 5 for p in points):
#             return [], "No clear thesis points extracted."

#         return points, None
#     except Exception as e:
#         return [], f"Error extracting key thesis points: {str(e)}"
def extract_key_thesis_points(vectordb, num_docs):
    if not vectordb:
        return [], "VectorDB is missing"

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,
    )

    k_value = min(50, num_docs) if num_docs > 0 else 1
    retriever = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={"k": k_value}), llm=llm)

    prompt = get_key_thesis_points_prompt_template()
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt
        | llm
        | StrOutputParser()
    )

    try:
        key_points_raw = chain.invoke("Extract unique and important investment points from the provided documents, distinct from a typical 3-paragraph thesis.")
        key_points = [point.strip().lstrip('- ').strip() for point in key_points_raw.split('\n') if point.strip()]
        return key_points, None

    except Exception as e:
        return [], f"Error extracting key thesis points: {str(e)}"


# def elaborate_on_thesis_point(vectordb, point_summary, num_docs, word_count):
#     """
#     Retrieves detailed information for a specific key thesis point.
#     Args:
#         vectordb: FAISS vector store.
#         point_summary: Summary of the thesis point.
#         num_docs: Number of documents in vector store.
#         word_count: Desired word count for the response.
#     Returns:
#         Tuple: (detailed text with citations, source documents, error message if any).
#     """
#     if not vectordb:
#         return "No documents analyzed.", [], "No documents analyzed."

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=GOOGLE_API_KEY,
#         temperature=0.0,
#     )

#     k_value = min(50, num_docs) if num_docs > 0 else 1
#     cache_key = f"retriever_thesis_point_{point_summary}_{'|'.join(session_state.processed_file_hashes)}"
#     if cache_key in session_state.cache:
#         retriever_docs = session_state.cache[cache_key]
#     else:
#         base_retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
#         retriever_docs = base_retriever.invoke(point_summary)
#         session_state.cache[cache_key] = retriever_docs

#     chain = (
#         RunnableParallel(
#             {"context": lambda x: retriever_docs, "point_summary": RunnablePassthrough(), "word_count": RunnablePassthrough()}
#         )
#         | RunnableParallel(
#             {"answer": get_detailed_explanation_prompt_template() | llm | StrOutputParser(), "source_documents": lambda x: retriever_docs}
#         )
#     )

#     try:
#         response = chain.invoke({"point_summary": point_summary, "word_count": word_count})
#         detail = response["answer"].strip()
#         sources = response.get("source_documents", [])

#         if not detail or len(detail) < 20 or any(keyword in detail.lower() for keyword in ["not found", "not available", "insufficient information", "could not generate"]):
#             return f"Detailed information for '{point_summary}' was not found.", [], "Information not found."

#         annotated_detail = add_inline_citations(detail, sources)
#         return annotated_detail, sources, None
#     except Exception as e:
#         error_msg = f"Error elaborating on thesis point: {str(e)}"
#         if "quota" in str(e).lower():
#             error_msg += " API quota exceeded."
#         return "An error occurred.", [], error_msg
def elaborate_on_thesis_point(
    point_summary: str,
    word_count: int,
    vectordb,
    num_docs: int
) -> Tuple[str, list, Optional[str]]:
    """
    Elaborate a thesis point using RAG (LLM + vectorstore).
    Returns (elaborated_text, sources, error)
    """
    try:
        if not GOOGLE_API_KEY:
            return "", [], "Google API key is missing or invalid."

        if vectordb is None:
            return "", [], "Vector store is not initialized."

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.0
        )

        k_value = min(30, num_docs) if num_docs > 0 else 1
        retriever = MultiQueryRetriever.from_llm(
            retriever=vectordb.as_retriever(search_kwargs={"k": k_value}),
            llm=llm
        )
        retrieved_docs = retriever.invoke(point_summary)

        prompt_template = PromptTemplate.from_template(
            """
            You are an equity research analyst. Based ONLY on the context below, elaborate this investment thesis point into a single paragraph (~{word_count} words) in professional style.

            Thesis Point:
            {point_summary}

            Context:
            {context}

            Elaborated Thesis Point:
            """
        )

        doc_chain = create_stuff_documents_chain(llm, prompt_template)

        rag_chain = {
            "context": lambda _: retrieved_docs,
            "point_summary": RunnablePassthrough(),
            "word_count": lambda _: word_count
        } | doc_chain

        response = rag_chain.invoke(point_summary)
        annotated_text = add_inline_citations(response.strip(), retrieved_docs)
        return annotated_text, retrieved_docs, None

    except Exception as e:
        return "", [], f"Error during elaboration: {str(e)}"

def conversational_retrieval(vectordb, files, query, history):
    """
    Retrieve relevant documents for conversational context, filtered by selected files.
    """
    if not vectordb or not vectordb.docstore._dict:
        return []

    # Get all documents from the vector store and filter by source (filename)
    all_vectordb_docs = [doc for doc_id, doc in vectordb.docstore._dict.items()]
    relevant_docs_for_filter = [doc for doc in all_vectordb_docs if doc.metadata.get("source") in files]

    if not relevant_docs_for_filter:
        return []

    # Initialize LLM for the retriever, consistent with FinanceBot's LLM
    llm_for_retriever = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", # ENSURE THIS IS SET TO GEMINI 2.5 FLASH
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )
    
    # Use MultiQueryRetriever for query generation
    retriever = MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(search_kwargs={"k": 10}), # Use k=10 for consistent retrieval depth
        llm=llm_for_retriever
    )
    
    # Combine history and query for context for MultiQueryRetriever
    context_for_multiquery = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nUser: {query}"
    
    # Get relevant documents
    results = retriever.get_relevant_documents(context_for_multiquery)
    
    # Final filter to ensure retrieved docs match selected files (important if vectordb is global/large)
    return [doc for doc in results if doc.metadata.get("source") in files]


# def conversational_retrieval(vectordb, files, query, history):
#     """
#     Retrieve relevant documents for conversational context, filtered by selected files.
#     """
#     # Filter documents based on selected files
#     relevant_docs = [doc for doc in vectordb.docstore._dict.values() if doc.metadata["source"] in files]
#     if not relevant_docs:
#         return []

#     # Use MultiQueryRetriever to handle conversational context
#     retriever = MultiQueryRetriever.from_llm(

#         retriever=vectordb.as_retriever(),

#         llm= ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0.2,
#         #include_original_query=True,

#     ))
#     # Combine history and query for context
#     context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nuser: {query}"
#     results = retriever.get_relevant_documents(context)
#     # Filter results to ensure they match selected files
#     return [doc for doc in results if doc.metadata["source"] in files]

def format_sources_for_display(source_documents):
    """
    Formats a list of Document objects into a readable string of unique sources.
    Args:
        source_documents: List of Document objects.
    Returns:
        Formatted string of sources.
    """
    if not source_documents:
        return "No direct sources found."

    unique_sources = {}
    for doc in source_documents:
        source = doc.metadata.get("source", "Unknown Document")
        page = doc.metadata.get("page", None)
        doc_type = doc.metadata.get("type", "text")
        key = (source, page, doc_type)
        if key not in unique_sources:
            unique_sources[key] = (source, page, doc_type)
    
    formatted_list = []
    sorted_unique_sources = sorted(list(unique_sources.values()), key=lambda x: (x[0], x[1], x[2]))

    for source, page, doc_type in sorted_unique_sources:
        if page is not None:
            formatted_list.append(f"{source} (Page: {page}, Type: {doc_type.capitalize()})")
        else:
            formatted_list.append(f"{source} (Type: {doc_type.capitalize()})")
            
    return "\n".join(formatted_list)

def convert_units(text, conversion_profile, custom_mappings=None):
    """
    Converts unit symbols in the text based on the conversion profile.
    Args:
        text: Input text to convert.
        conversion_profile: Conversion profile ('Default', 'Words to Symbols', 'Custom').
        custom_mappings: Optional custom unit mappings.
    Returns:
        Text with converted units.
    """
    if not text or not isinstance(text, str):
        return text

    citation_placeholders = {}
    def replace_citation(match):
        placeholder_id = f"CITATION_PLACEHOLDER_{len(citation_placeholders)}"
        citation_placeholders[placeholder_id] = match.group(0)
        return placeholder_id

    text_with_placeholders = re.sub(r'<sup[^>]*?>.*?</sup>', replace_citation, text)

    conversion_profiles = {
        "Default": {
            "%": "percentage", "~": "approximately", "$": "US dollar", "(Y/Y)": "year-on-year",
            "€": "Euro", "million": "M", "<": "less than", ">": "greater than"
        },
        "Words to Symbols": {
            "%": "%", "~": "~", "$": "$", "(Y/Y)": "(Y/Y)",
            "€": "€", "million": "million", "<": "<", ">": ">"
        },
        "Custom": custom_mappings if custom_mappings else {}
    }

    if conversion_profile not in conversion_profiles:
        conversion_profile = "Default"
    current_mappings = conversion_profiles.get(conversion_profile, conversion_profiles["Default"])

    if not current_mappings or not any(current_mappings.values()):
        for placeholder, original_citation_html in citation_placeholders.items():
            text_with_placeholders = text_with_placeholders.replace(placeholder, original_citation_html)
        return text_with_placeholders

    modified_text = text_with_placeholders
    conversion_rules = []

    for symbol, word in current_mappings.items():
        if not symbol or not word or not symbol.strip() or not word.strip():
            continue
        escaped_symbol = re.escape(symbol)
        conversion_rules.append((rf"(\d+(?:,\d+)?(?:\.\d+)?)\s*{escaped_symbol}(?![^\s(]*\))", rf"\1 {word}"))
        conversion_rules.append((rf"\({escaped_symbol}\s*(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:[^\)]+)?\)", rf"(\1 {word})"))
        conversion_rules.append((rf"\b{escaped_symbol}\s*(\d+(?:,\d+)?(?:\.\d+)?)", rf"{word}\1"))
        conversion_rules.append((rf"\b{escaped_symbol}\b(?!\s*\d)", word))
        conversion_rules.append((rf"\b{re.escape(word)}\b(?!\s*{escaped_symbol})", symbol))
        if symbol == "~":
            conversion_rules.append((rf"(\d+(?:,\d+)?(?:\.\d+)?)\s*approximately", rf"{symbol}\1"))
            conversion_rules.append((rf"approximately\s*(\d+(?:,\d+)?(?:\.\d+)?)", rf"{symbol}\1"))

    conversion_rules.sort(key=lambda x: len(x[0]), reverse=True)
    for pattern, replacement in conversion_rules:
        modified_text = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)

    for placeholder, original_citation_html in citation_placeholders.items():
        modified_text = modified_text.replace(placeholder, original_citation_html)

    return modified_text

