// import React, { useState, useEffect } from 'react';
// import { Document, Page, pdfjs } from 'react-pdf';
// import 'react-pdf/dist/Page/AnnotationLayer.css';
// import 'react-pdf/dist/Page/TextLayer.css';
// import axios from 'axios';
// const InlinePDFViewer = ({ file, page, blobUrl }) => {

// // Set pdf.js worker
// pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js`;

// const InlinePDFViewer = ({ file, page }) => {
//   const [numPages, setNumPages] = useState(null);
//   const [error, setError] = useState(null);
//   const [pdfData, setPdfData] = useState(null);

//   useEffect(() => {
//     const fetchPDF = async () => {
//       if (!file || !page) {
//         setError('Invalid file or page number');
//         console.error('Invalid props:', { file, page });
//         return;
//       }

//       setError(null);
//       console.log(`Fetching PDF for file: ${file}, page: ${page}`);
//       try {
//         const response = await axios.get(`/api/get-pdf/${encodeURIComponent(file)}`, {

//           responseType: 'arraybuffer', // Expect binary PDF data
//           timeout: 60000, // 60 seconds
//         });
//         console.log('PDF fetch response:', {
//           status: response.status,
//           headers: response.headers,
//           dataLength: response.data.byteLength,
//           contentType: response.headers['content-type'],
//         });

//         // Verify Content-Type
//         if (response.headers['content-type'] !== 'application/pdf') {
//           throw new Error(`Invalid Content-Type: ${response.headers['content-type']}`);
//         }

//         // Convert ArrayBuffer to Blob
//         const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
//         const pdfUrl = URL.createObjectURL(pdfBlob);
//         setPdfData(pdfUrl);
//       } catch (error) {
//         const errorDetails = {
//           message: error.message,
//           code: error.code,
//           response: error.response
//             ? {
//                 status: error.response.status,
//                 data: error.response.data ? new TextDecoder().decode(error.response.data) : null,
//                 headers: error.response.headers,
//               }
//             : null,
//         };
//         console.error('PDF fetch error:', errorDetails);
//         setError(
//           `Failed to fetch PDF: ${error.message}${error.response ? ` (Status: ${error.response.status})` : ''}`
//         );
//       }
//     };

//     fetchPDF();

//     // Cleanup Blob URL
//     return () => {
//       if (pdfData) {
//         URL.revokeObjectURL(pdfData);
//       }
//     };
//   }, [file, page, pdfData]);

//   const onDocumentLoadSuccess = ({ numPages }) => {
//     setNumPages(numPages);
//     setError(null);
//     console.log(`PDF loaded successfully: ${file}, ${numPages} pages`);
//   };

//   const onDocumentLoadError = (error) => {
//     console.error(`PDF render error: ${error.message}`);
//     setError(`Failed to render PDF: ${error.message}`);
//   };

//   return (
//     <div>
//       {error && <div style={{ color: 'red' }}>{error}</div>}
//       {pdfData && (
//         <Document
//           file={pdfData}
//           onLoadSuccess={onDocumentLoadSuccess}
//           onLoadError={onDocumentLoadError}
//         >
//           <Page pageNumber={page} />
//         </Document>
//       )}
//       {numPages && (
//         <p>
//           Page {page} of {numPages}
//         </p>
//       )}
//     </div>
//   );
// };

// export default InlinePDFViewer;


////////////////////////////////////////localstroage////////////////////////////////////////////////////////////////////////////

// import React, { useState } from 'react';
// import { Document, Page } from 'react-pdf';
// import { pdfjs } from 'react-pdf'; // ✅ Fix this import
// import 'react-pdf/dist/Page/AnnotationLayer.css';
// import 'react-pdf/dist/Page/TextLayer.css';

// // Set pdf.js worker
// pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

// const InlinePDFViewer = ({ file, page, blobUrl }) => {
//   const [numPages, setNumPages] = useState(null);
//   const [error, setError] = useState(null);

//   const onDocumentLoadSuccess = ({ numPages }) => {
//     setNumPages(numPages);
//     setError(null);
//     console.log(`PDF loaded successfully: ${file}, ${numPages} pages`);
//   };

//   const onDocumentLoadError = (error) => {
//     console.error(`PDF render error: ${error.message}`);
//     setError(`Failed to render PDF: ${error.message}`);
//   };

//   return (
//     <div>
//       {error && <div style={{ color: 'red' }}>{error}</div>}
//       {blobUrl && (
//         <Document
//           file={blobUrl}
//           onLoadSuccess={onDocumentLoadSuccess}
//           onLoadError={onDocumentLoadError}
//         >
//           <Page pageNumber={page} />
//         </Document>
//       )}
//       {numPages && (
//         <p>
//           Page {page} of {numPages}
//         </p>
//       )}
//     </div>
//   );
// };

// export default InlinePDFViewer;


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import React, { useEffect, useRef, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const InlinePDFViewer = ({ file, page, blobUrl }) => {
  const [numPages, setNumPages] = useState(null);
  const [error, setError] = useState(null);
  const pageRefs = useRef([]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setError(null);
  };

  const onDocumentLoadError = (error) => {
    setError(`Failed to render PDF: ${error.message}`);
  };

  // Scroll to specified page
  useEffect(() => {
    if (page && pageRefs.current[page - 1]) {
      pageRefs.current[page - 1].scrollIntoView({ behavior: 'smooth' });
    }
  }, [page]);

  return (
    <div style={{ height: '80vh', overflowY: 'auto' }}>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {blobUrl && (
        <Document
          file={blobUrl}
          onLoadSuccess={onDocumentLoadSuccess}
          onLoadError={onDocumentLoadError}
        >
          {Array.from(new Array(numPages), (_, i) => (
            <div key={i} ref={(el) => (pageRefs.current[i] = el)}>
              <Page pageNumber={i + 1} width={800} />
            </div>
          ))}
        </Document>
      )}
    </div>
  );
};

export default InlinePDFViewer;


//////////////////////////////////////////////////////////////////////////////////////////////////////////////

// inlinePDFviewer.jsx
// import React, { useEffect, useState, useRef } from "react";

// export default function InlinePDFViewer({ filename, page, highlight }) {
//   const [pages, setPages] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const containerRef = useRef(null);

//   useEffect(() => {
//     if (!filename) return;

//     setLoading(true);

//     fetch(`http://localhost:8000/full-pdf-text/${filename}`)
//       .then((res) => {
//         if (!res.ok) throw new Error("Failed to fetch PDF text");
//         return res.json();
//       })
//       .then((data) => {
//         if (data.status === "success") {
//           let processedPages = data.pages.map((text, index) => {
//             if (highlight && index === page) {
//               // Escape RegExp special chars in highlight text
//               const escaped = highlight.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
//               const regex = new RegExp(escaped, "gi");
//               return text.replace(regex, (match) => `<mark>${match}</mark>`);
//             }
//             return text;
//           });

//           setPages(processedPages);
//         } else {
//           console.error("Error:", data.message);
//         }
//       })
//       .catch((err) => {
//         console.error(err);
//       })
//       .finally(() => setLoading(false));
//   }, [filename, page, highlight]);

//   // Scroll to the target page after rendering
//   useEffect(() => {
//     if (!loading && containerRef.current && page != null) {
//       const target = containerRef.current.querySelector(`[data-page='${page}']`);
//       if (target) {
//         target.scrollIntoView({ behavior: "smooth", block: "start" });
//       }
//     }
//   }, [loading, page]);

//   if (loading) return <div>Loading full text...</div>;

//   return (
//     <div
//       ref={containerRef}
//       style={{
//         height: "80vh",
//         overflowY: "auto",
//         padding: "1rem",
//         backgroundColor: "#fff",
//       }}
//     >
//       {pages.map((text, index) => (
//         <div
//           key={index}
//           data-page={index}
//           style={{
//             borderBottom: "1px solid #ddd",
//             paddingBottom: "1rem",
//             marginBottom: "1rem",
//           }}
//           dangerouslySetInnerHTML={{ __html: `<pre>${text}</pre>` }}
//         />
//       ))}
//     </div>
//   );
// }
