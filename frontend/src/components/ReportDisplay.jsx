// import React from 'react';
// import { Card, CardContent, Typography, Box } from '@mui/material';
// import '../App.css';

// const LazyLoadWrapper = ({ children }) => children;

// const ReportDisplay = ({ reportData, onCitationClick, uploadedFileNames }) => {
//   console.log('reportData:', reportData); // Debug reportData

//   const parseCitations = (text) => {
//     if (!text) return text;

//     // Use first uploaded filename or fallback
//     const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';

//     // Regex for <sup>[1]</sup> or <span> citations
//     const citationRegex = /(<sup>\[(\d+)\]<\/sup>)|(<span class='citation' onclick="openPDF\('([^']+)',\s*'([^']+)',\s*'[^']*'\)">(.*?)<span class='citation-card'>.*?<\/span><\/span>)/g;

//     let elements = [];
//     let lastIndex = 0;

//     while ((match = citationRegex.exec(text)) !== null) {
//       const [fullMatch, supMatch, citationNumberSup, spanMatch, file, page, citationText] = match;
//       const startIndex = match.index;

//       if (startIndex > lastIndex) {
//         elements.push(text.slice(lastIndex, startIndex));
//       }

//       let displayText, fileToUse, pageNum;

//       if (supMatch && citationNumberSup) {
//         displayText = `[${citationNumberSup}]`;
//         fileToUse = fileName; // Use uploaded filename
//         pageNum = parseInt(citationNumberSup); // Assume page matches citation number
//       } else if (spanMatch && file && page) {
//         displayText = citationText;
//         fileToUse = file;
//         pageNum = parseInt(page);
//       } else {
//         elements.push(fullMatch);
//         lastIndex = startIndex + fullMatch.length;
//         continue;
//       }

//       elements.push(
//         <span
//           key={startIndex}
//           className="citation"
//           onClick={() => fileToUse && pageNum && onCitationClick({ file: fileToUse, page: pageNum })}
//           style={{ cursor: fileToUse ? 'pointer' : 'default', color: fileToUse ? '#1976D2' : 'inherit' }}
//         >
//           {displayText}
//         </span>
//       );

//       lastIndex = startIndex + fullMatch.length;
//     }

//     if (lastIndex < text.length) {
//       elements.push(text.slice(lastIndex));
//     }

//     return elements;
//   };

//   const companyName = typeof reportData?.company_name === 'string' ? reportData.company_name : reportData?.company_name?.[0] || 'N/A';

//   return (
//     <Box className="section-card">
//       <LazyLoadWrapper>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Company Name</Typography>
//             <Typography variant="body1">{companyName}</Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Business Overview</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.business_overview)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Quarterly Highlights</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.quarterly_highlights)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Investment Thesis</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.investment_thesis)}
//             </Typography>
//           </CardContent>
//         </Card>
//       </LazyLoadWrapper>
//     </Box>
//   );
// };

// export default ReportDisplay;



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// import React from 'react';
// import { Card, CardContent, Typography, Box } from '@mui/material';
// import '../App.css';
// import KeyThesisPoints from './KeyThesisPoints'; // adjust path if needed


// const LazyLoadWrapper = ({ children }) => children;

// const ReportDisplay = ({ reportData, onCitationClick, uploadedFileNames }) => {
//   console.log('reportData:', reportData); // Debug reportData

//   const parseCitations = (text) => {
//     if (!text) return text;

//     // Use first uploaded filename or fallback
//     const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';

//     // Regex for <sup>[1]</sup> or <span> citations
//     const citationRegex = /(<sup>\[(\d+)\]<\/sup>)|(<span class='citation' onclick="openPDF\('([^']+)',\s*'([^']+)',\s*'[^']*'\)">(.*?)<span class='citation-card'>.*?<\/span><\/span>)/g;

//     let elements = [];
//     let lastIndex = 0;

//     let match; // Declare match to fix no-undef
//     while ((match = citationRegex.exec(text)) !== null) {
//       const [fullMatch, supMatch, citationNumberSup, spanMatch, file, page, citationText] = match;
//       const startIndex = match.index;

//       if (startIndex > lastIndex) {
//         elements.push(text.slice(lastIndex, startIndex));
//       }

//       let displayText, fileToUse, pageNum;

//       if (supMatch && citationNumberSup) {
//         displayText = `[${citationNumberSup}]`;
//         fileToUse = fileName; // Use uploaded filename
//         pageNum = parseInt(citationNumberSup); // Assume page matches citation number
//       } else if (spanMatch && file && page) {
//         displayText = citationText;
//         fileToUse = file;
//         pageNum = parseInt(page);
//       } else {
//         elements.push(fullMatch);
//         lastIndex = startIndex + fullMatch.length;
//         continue;
//       }

//       elements.push(
//         <span
//           key={startIndex}
//           className="citation"
//           onClick={() => fileToUse && pageNum && onCitationClick({ file: fileToUse, page: pageNum })}
//           style={{ cursor: fileToUse ? 'pointer' : 'default', color: fileToUse ? '#1976D2' : 'inherit' }}
//         >
//           {displayText}
//         </span>
//       );

//       lastIndex = startIndex + fullMatch.length;
//     }

//     if (lastIndex < text.length) {
//       elements.push(text.slice(lastIndex));
//     }

//     return elements;
//   };

//   const companyName = typeof reportData?.company_name === 'string' ? reportData.company_name : reportData?.company_name?.[0] || 'N/A';

//   return (
//     <Box className="section-card">
//       <LazyLoadWrapper>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Company Name</Typography>
//             <Typography variant="body1">{companyName}</Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Business Overview</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.business_overview)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Quarterly Highlights</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.quarterly_highlights)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Investment Thesis</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.investment_thesis)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//   <CardContent>
//     <Typography variant="h3">Investment Thesis</Typography>
//     <Typography variant="body1" component="span">
//       {parseCitations(reportData?.investment_thesis)}
//     </Typography>
//   </CardContent>
// </Card>

// {reportData?.key_thesis_points && (
//   <Card>
//     <CardContent>
//       <KeyThesisPoints keyThesisPoints={reportData.key_thesis_points} />
//     </CardContent>
//   </Card>
// )}

//       </LazyLoadWrapper>
//     </Box>
//   );


// };

// export default ReportDisplay;


//////////////////////////////////////////////////////////////////////////////////////////////////////



// import { Card, CardContent, Typography, Box } from '@mui/material';
// import KeyThesisPoints from './KeyThesisPoints'; // ✅ Add this import
// import '../App.css';
// import React, { useState } from 'react';
// import ChatBox from './ChatBox';


// const LazyLoadWrapper = ({ children }) => children;
// const [selectedPDF, setSelectedPDF] = useState(null);

// const ReportDisplay = ({ reportData, onCitationClick, uploadedFileNames, pdfBlobs }) => {

//   console.log('reportData:', reportData); // Debug reportData
//   console.log("Received key thesis points:", reportData?.key_thesis_points); // ✅ New line
//  // Debug reportData

//  const parseCitations = (text) => {
//   if (!text) return text;

//   const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';

//   // Match: <sup><span class='citation' data-source=... data-page=...>[1]<span class='citation-card'>...</span></span></sup>
//   const citationRegex = /<sup><span class='citation'[^>]*data-source='([^']+)'[^>]*data-page='([^']+)'[^>]*>\[(\d+)\](?:<span class='citation-card'>.*?<\/span>)?<\/span><\/sup>/g;

//   let elements = [];
//   let lastIndex = 0;
//   let match;

//   while ((match = citationRegex.exec(text)) !== null) {
//     const [fullMatch, sourceFile, pageNum, citationNumber] = match;
//     const startIndex = match.index;

//     // Push text before the match
//     if (startIndex > lastIndex) {
//       elements.push(text.slice(lastIndex, startIndex));
//     }

//     // Push only the [number] part as clickable
//     elements.push(
//       <span
//         key={startIndex}
//         className="citation"
//         // onClick={() =>
//         //   onCitationClick({
//         //     file: sourceFile || fileName,
//         //     page: parseInt(pageNum),
//         //   })
//         // }
//         onClick={() => {//////////////////////////////////////for localstroage////////////////////////////////////////////
//           const blobUrl = pdfBlobs?.[sourceFile];
//           if (!blobUrl) {
//             alert("PDF not available in memory.");
//             return;
//           }
//           setSelectedPDF({ file: sourceFile, page: parseInt(pageNum), blobUrl });
//         }}        
     

//         style={{ cursor: 'pointer', color: '#1976D2' }}
//       >
//         [{citationNumber}]
//       </span>
//     );

//     lastIndex = startIndex + fullMatch.length;
//   }

//   // Push remaining text
//   if (lastIndex < text.length) {
//     elements.push(text.slice(lastIndex));
//   }

//   return elements;
// };



//   const companyName = typeof reportData?.company_name === 'string' ? reportData.company_name : reportData?.company_name?.[0] || 'N/A';
//   const [thesisPoints, setThesisPoints] = useState(reportData?.key_thesis_points || []);
//   const sessionId = reportData?.session_id || "default_session";
// const fileNames = reportData?.uploadedFileNames || [];



//   return (
//     <Box className="section-card">
//       <LazyLoadWrapper>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Company Name</Typography>
//             <Typography variant="body1">{companyName}</Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Business Overview</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.business_overview)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Quarterly Highlights</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.quarterly_highlights)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Investment Thesis</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.investment_thesis)}
//             </Typography>
//           </CardContent>
//         </Card>

//         {/* ✅ New Key Thesis Points section */}
//         {Array.isArray(thesisPoints) && (
//   <Card>
//     <CardContent>
//       <KeyThesisPoints
//         keyThesisPoints={thesisPoints}
//         taskId={reportData.task_id}
//         onUpdate={setThesisPoints}
//       />
//     </CardContent>
//   </Card>
// )}
// <ChatBox sessionId={sessionId} fileNames={fileNames} />

// {selectedPDF && (
//   <InlinePDFViewer
//     file={selectedPDF.file}
//     page={selectedPDF.page}
//     blobUrl={selectedPDF.blobUrl}
//   />
// )}


//       </LazyLoadWrapper>
//     </Box>
//   );
// };

// export default ReportDisplay;


/////////////////////////////////////localstroage////////////////////////////////////////////////////////////////////////////

// import { Card, CardContent, Typography, Box } from '@mui/material';
// import KeyThesisPoints from './KeyThesisPoints';
// import '../App.css';
// import React, { useState } from 'react';
// import ChatBox from './ChatBox';
// import InlinePDFViewer from './inlinePDFviewer'; // ✅ Don't forget this import!
// import Tooltip from '@mui/material/Tooltip';

// const LazyLoadWrapper = ({ children }) => children;

// const ReportDisplay = ({ reportData, uploadedFileNames, pdfBlobs }) => {
//   console.log("reportData.task_id in ReportDisplay:", reportData?.task_id);

//   const [thesisPoints, setThesisPoints] = useState(reportData?.key_thesis_points || []);
//   const [selectedPDF, setSelectedPDF] = useState(null); // ✅ Now it's inside the component

//   const sessionId = reportData?.session_id || "default_session";
//   const fileNames = reportData?.uploadedFileNames || [];

//   const companyName =
//     typeof reportData?.company_name === 'string'
//       ? reportData.company_name
//       : reportData?.company_name?.[0] || 'N/A';

//       // console.log("✅ reportData.task_id in ReportDisplay:", reportData?.task_id);

//   const parseCitations = (text) => {
//     if (!text) return text;

//     const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';
//     const citationRegex = /<sup><span class='citation'[^>]*data-source='([^']+)'[^>]*data-page='([^']+)'[^>]*data-context='([^']*)'[^>]*>\[(\d+)\](?:<span class='citation-card'>.*?<\/span>)?<\/span><\/sup>/g;

//     let elements = [];
//     let lastIndex = 0;
//     let match;

//     while ((match = citationRegex.exec(text)) !== null) {
//       const [fullMatch, sourceFile, pageNum, context, citationNumber] = match;
//       const startIndex = match.index;

//       if (startIndex > lastIndex) {
//         elements.push(text.slice(lastIndex, startIndex));
//       }

//       elements.push(
//         // import Tooltip from '@mui/material/Tooltip';

// <Tooltip
//   title={
//     <div>
//       <div><strong>Source:</strong> {sourceFile}</div>
//       <div><strong>Page:</strong> {pageNum}</div>
//       <div><strong>Context:</strong> {context}</div>
//     </div>
//   }
//   arrow
//   componentsProps={{
//     tooltip: {
//       sx: {
//         fontSize: '1rem', // 🔼 Increase this value as needed (e.g., '1.2rem', '16px')
//         maxWidth: 400,     // Optional: make sure long context doesn't wrap too early
//         whiteSpace: 'pre-line',
//       },
//     },
//   }}
// >
//   <span
//     onClick={() => {
//       const blobUrl = pdfBlobs?.[sourceFile];
//       if (!blobUrl) {
//         alert("PDF not available in memory.");
//         return;
//       }
//       setSelectedPDF({ file: sourceFile, page: parseInt(pageNum), blobUrl });
//     }}
//     style={{ cursor: 'pointer', color: '#1976D2', textDecoration: 'underline dotted' }}
//   >
//     [{citationNumber}]
//   </span>
// </Tooltip>

//       );
      
      

//       lastIndex = startIndex + fullMatch.length;
//     }

//     if (lastIndex < text.length) {
//       elements.push(text.slice(lastIndex));
//     }

//     return elements;
//   };
//   console.log("✅ reportData.task_id in ReportDisplay:", reportData?.task_id);
//   return (
//     <Box className="section-card">
//       <LazyLoadWrapper>
//         <Card>
//           <CardContent>
//             <Typography variant="h3">Company Name</Typography>
//             <Typography variant="body1">{companyName}</Typography>
//           </CardContent>
//         </Card>

//         <Card>
//           <CardContent>
//             <Typography variant="h3">Business Overview</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.business_overview)}
//             </Typography>
//           </CardContent>
//         </Card>

//         <Card>
//           <CardContent>
//             <Typography variant="h3">Quarterly Highlights</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.quarterly_highlights)}
//             </Typography>
//           </CardContent>
//         </Card>

//         <Card>
//           <CardContent>
//             <Typography variant="h3">Investment Thesis</Typography>
//             <Typography variant="body1" component="span">
//               {parseCitations(reportData?.investment_thesis)}
//             </Typography>
//           </CardContent>
//         </Card>
//         {/* console.log("✅ reportData.task_id in ReportDisplay:", reportData?.task_id); */}
//         {Array.isArray(thesisPoints) && (
//           <Card>
//             <CardContent>
//               <KeyThesisPoints
              
//                 keyThesisPoints={thesisPoints}
//                 taskId={reportData.task_id}
//                 onUpdate={setThesisPoints}
//               />
//             </CardContent>
//           </Card>
//         )}

//         <ChatBox sessionId={sessionId} fileNames={fileNames} />

//         {selectedPDF && (
//           <InlinePDFViewer
//             file={selectedPDF.file}
//             page={selectedPDF.page}
//             blobUrl={selectedPDF.blobUrl}
//           />
//         )}
//       </LazyLoadWrapper>
//     </Box>
//   );
// };

// export default ReportDisplay;


///////////////////////////////////////////////////////////////////////GROK/////////////////////////////////////////////////////////////



// import { Card, CardContent, Typography, Box } from '@mui/material';
// import KeyThesisPoints from './KeyThesisPoints';
// import '../App.css';
// import React, { useState } from 'react';
// import ChatBox from './ChatBox';
// import InlinePDFViewer from './inlinePDFviewer';
// import Tooltip from '@mui/material/Tooltip';

// const LazyLoadWrapper = ({ children }) => children;

// const ReportDisplay = ({ reportData, uploadedFileNames, pdfBlobs }) => {
//   console.log("reportData.task_id in ReportDisplay:", reportData?.task_id);
//   const [thesisPoints, setThesisPoints] = useState(reportData?.key_thesis_points || []);
//   const [selectedPDF, setSelectedPDF] = useState(null);
//   const sessionId = reportData?.session_id || "default_session";
//   const fileNames = reportData?.uploadedFileNames || [];

//   const companyName =
//     typeof reportData?.company_name === 'string'
//       ? reportData.company_name
//       : reportData?.company_name?.[0] || 'N/A';

//   const parseCitations = (text) => {
//     if (!text) return text;

//     const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';
//     const citationRegex = /<sup><span class='citation'[^>]*data-source='([^']+)'[^>]*data-page='([^']+)'[^>]*data-context='([^']*)'[^>]*>\[(\d+)\](?:<span class='citation-card'>.*?<\/span>)?<\/span><\/sup>/g;

//     let elements = [];
//     let lastIndex = 0;
//     let match;

//     while ((match = citationRegex.exec(text)) !== null) {
//       const [fullMatch, sourceFile, pageNum, context, citationNumber] = match;
//       const startIndex = match.index;

//       if (startIndex > lastIndex) {
//         elements.push(text.slice(lastIndex, startIndex));
//       }

//       elements.push(
//         <Tooltip
//           title={
//             <div>
//               <div><strong>Source:</strong> {sourceFile}</div>
//               <div><strong>Page:</strong> {pageNum}</div>
//               <div><strong>Context:</strong> {context}</div>
//             </div>
//           }
//           arrow
//           componentsProps={{
//             tooltip: {
//               sx: {
//                 fontSize: '1rem',
//                 maxWidth: 400,
//                 whiteSpace: 'pre-line',
//                 bgcolor: '#424242', /* Dark tooltip background */
//                 color: '#ffffff', /* White text */
//               },
//             },
//           }}
//         >
//           <span
//             onClick={() => {
//               const blobUrl = pdfBlobs?.[sourceFile];
//               if (!blobUrl) {
//                 alert("PDF not available in memory.");
//                 return;
//               }
//               setSelectedPDF({ file: sourceFile, page: parseInt(pageNum), blobUrl });
//             }}
//             style={{ cursor: 'pointer', color: '#42a5f5', textDecoration: 'underline dotted' }}
//           >
//             [{citationNumber}]
//           </span>
//         </Tooltip>
//       );

//       lastIndex = startIndex + fullMatch.length;
//     }

//     if (lastIndex < text.length) {
//       elements.push(text.slice(lastIndex));
//     }

//     return elements;
//   };

//   return (
//     <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//       <LazyLoadWrapper>
//         <Card sx={{ bgcolor: 'background.paper' }}>
//           <CardContent>
//             <Typography variant="h3" color="text.primary">Company Name</Typography>
//             <Typography variant="body1" color="text.secondary">{companyName}</Typography>
//           </CardContent>
//         </Card>
//         <Card sx={{ bgcolor: 'background.paper' }}>
//           <CardContent>
//             <Typography variant="h3" color="text.primary">Business Overview</Typography>
//             <Typography variant="body1" component="span" color="text.secondary">
//               {parseCitations(reportData?.business_overview)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card sx={{ bgcolor: 'background.paper' }}>
//           <CardContent>
//             <Typography variant="h3" color="text.primary">Quarterly Highlights</Typography>
//             <Typography variant="body1" component="span" color="text.secondary">
//               {parseCitations(reportData?.quarterly_highlights)}
//             </Typography>
//           </CardContent>
//         </Card>
//         <Card sx={{ bgcolor: 'background.paper' }}>
//           <CardContent>
//             <Typography variant="h3" color="text.primary">Investment Thesis</Typography>
//             <Typography variant="body1" component="span" color="text.secondary">
//               {parseCitations(reportData?.investment_thesis)}
//             </Typography>
//           </CardContent>
//         </Card>
//         {Array.isArray(thesisPoints) && (
//           <Card sx={{ bgcolor: 'background.paper' }}>
//             <CardContent>
//               <KeyThesisPoints
//                 keyThesisPoints={thesisPoints}
//                 taskId={reportData.task_id}
//                 onUpdate={setThesisPoints}
//               />
//             </CardContent>
//           </Card>
//         )}
//         {selectedPDF && (
//           <Card sx={{ bgcolor: 'background.paper' }}>
//             <CardContent>
//               <InlinePDFViewer
//                 file={selectedPDF.file}
//                 page={selectedPDF.page}
//                 blobUrl={selectedPDF.blobUrl}
//               />
//             </CardContent>
//           </Card>
//         )}
//       </LazyLoadWrapper>
//     </Box>
//   );
// };

// export default ReportDisplay;


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import React, { useState } from 'react';
import { Card, CardContent, Typography, Box, Divider } from '@mui/material';
import KeyThesisPoints from './KeyThesisPoints';
import ModifySection from './ModifySection';
import UnitConverter from './UnitConverter';
import PDFDownloader from './PDFDownloader';
import Tooltip from '@mui/material/Tooltip';
import '../App.css';

const LazyLoadWrapper = ({ children }) => children;

const ReportDisplay = ({
  reportData,
  uploadedFileNames,
  pdfBlobs,
  onCitationClick,
  showModifySection,
  showUnitConverter,
  showPDFDownloader,
  taskId,
  onReportGenerated,
  onError,
}) => {
  const [thesisPoints, setThesisPoints] = useState(reportData?.key_thesis_points || []);
  const companyName =
    typeof reportData?.company_name === 'string'
      ? reportData.company_name
      : reportData?.company_name?.[0] || 'N/A';

  const parseCitations = (text) => {
    if (!text) return text;

    const fileName = uploadedFileNames?.[0] || 'uploaded.pdf';
    const citationRegex = /<sup><span class='citation'[^>]*data-source='([^']+)'[^>]*data-page='([^']+)'[^>]*data-context='([^']*)'[^>]*>\[(\d+)\](?:<span class='citation-card'>.*?<\/span>)?<\/span><\/sup>/g;

    let elements = [];
    let lastIndex = 0;
    let match;

    while ((match = citationRegex.exec(text)) !== null) {
      const [fullMatch, sourceFile, pageNum, context, citationNumber] = match;
      const startIndex = match.index;

      if (startIndex > lastIndex) {
        elements.push(text.slice(lastIndex, startIndex));
      }

      elements.push(
        <Tooltip
          title={
            <div>
              <div><strong>Source:</strong> {sourceFile}</div>
              <div><strong>Page:</strong> {pageNum}</div>
              <div><strong>Context:</strong> {context}</div>
            </div>
          }
          arrow
          componentsProps={{
            tooltip: {
              sx: {
                fontSize: '1rem',
                maxWidth: 400,
                whiteSpace: 'pre-line',
                bgcolor: '#424242', /* Dark tooltip background */
                color: '#ffffff', /* White text */
              },
            },
          }}
        >
          <span
            onClick={() => {
              const blobUrl = pdfBlobs?.[sourceFile];
              if (!blobUrl) {
                alert("PDF not available in memory.");
                return;
              }
              onCitationClick({ file: sourceFile, page: parseInt(pageNum) });
            }}
            style={{ cursor: 'pointer', color: '#42a5f5', textDecoration: 'underline dotted' }}
          >
            [{citationNumber}]
          </span>
        </Tooltip>
      );

      lastIndex = startIndex + fullMatch.length;
    }

    if (lastIndex < text.length) {
      elements.push(text.slice(lastIndex));
    }

    return elements;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, bgcolor: '#27292D', p: 2 }}>
      <LazyLoadWrapper>
        <Card sx={{ bgcolor: 'background.paper' }}>
          <CardContent>
            <Typography variant="h3" color="text.primary">Company Name</Typography>
            <Typography variant="body1" color="text.secondary">{companyName}</Typography>
          </CardContent>
        </Card>
        <Card sx={{ bgcolor: 'background.paper' }}>
          <CardContent>
            <Typography variant="h3" color="text.primary">Business Overview</Typography>
            <Typography variant="body1" component="span" color="text.secondary">
              {parseCitations(reportData?.business_overview)}
            </Typography>
          </CardContent>
        </Card>
        <Card sx={{ bgcolor: 'background.paper' }}>
          <CardContent>
            <Typography variant="h3" color="text.primary">Quarterly Highlights</Typography>
            <Typography variant="body1" component="span" color="text.secondary">
              {parseCitations(reportData?.quarterly_highlights)}
            </Typography>
          </CardContent>
        </Card>
        <Card sx={{ bgcolor: 'background.paper' }}>
          <CardContent>
            <Typography variant="h3" color="text.primary">Investment Thesis</Typography>
            <Typography variant="body1" component="span" color="text.secondary">
              {parseCitations(reportData?.investment_thesis)}
            </Typography>
          </CardContent>
        </Card>
        {Array.isArray(thesisPoints) && (
          <Card sx={{ bgcolor: 'background.paper' }}>
            <CardContent>
              <KeyThesisPoints
                keyThesisPoints={thesisPoints}
                taskId={reportData.task_id}
                onUpdate={setThesisPoints}
              />
            </CardContent>
          </Card>
        )}
        {showModifySection && (
          <>
            <Divider sx={{ mb: 2, bgcolor: '#424242' }} />
            <ModifySection
              taskId={taskId}
              onReportGenerated={onReportGenerated}
              onError={onError}
            />
          </>
        )}
        {showUnitConverter && (
          <>
            <Divider sx={{ mb: 2, bgcolor: '#424242' }} />
            <UnitConverter
              onReportGenerated={onReportGenerated}
              onError={onError}
            />
          </>
        )}
        {showPDFDownloader && (
          <>
            <Divider sx={{ mb: 2, bgcolor: '#424242' }} />
            <PDFDownloader
              reportData={reportData}
              onError={onError}
            />
          </>
        )}
      </LazyLoadWrapper>
    </Box>
  );
};

export default ReportDisplay;

















































































































