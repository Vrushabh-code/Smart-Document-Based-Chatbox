// import React, { useState, useRef, useEffect } from 'react';
// import { 
//   Box, 
//   TextField, 
//   Button, 
//   Typography, 
//   Paper, 
//   Avatar, 
//   CircularProgress,
//   Fade
// } from '@mui/material';
// import { Send as SendIcon } from '@mui/icons-material';
// import axios from 'axios';

// const ChatBox = ({ sessionId, fileNames }) => {
//   const [query, setQuery] = useState('');
//   const [messages, setMessages] = useState([
//     {
//       role: 'assistant',
//       content: 'Hello! I\'m your PDF assistant. Ask me anything about your document.'
//     }
//   ]);
//   const [isLoading, setIsLoading] = useState(false);
//   const messagesEndRef = useRef(null);

//   // Auto-scroll to bottom of chat
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const handleSend = async () => {
//     if (!query.trim()) return;

//     const userMessage = { role: 'user', content: query };
//     const updatedMessages = [...messages, userMessage];
    
//     setMessages(updatedMessages);
//     setQuery('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://127.0.0.1:8000/api/chat', {
//         session_id: sessionId,
//         files: fileNames,
//         query: query,
//         history: JSON.stringify(updatedMessages.filter(msg => msg.role !== 'system'))
//       });

//       setMessages(prev => [...prev, {
//         role: 'assistant',
//         content: response.data.response
//       }]);
//     } catch (err) {
//       console.error('Chat error:', err);
//       setMessages(prev => [...prev, {
//         role: 'assistant',
//         content: 'Sorry, I encountered an error. Please try again.'
//       }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyDown = (e) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   return (
//     <Paper 
//       elevation={3} 
//       sx={{
//         height: '100%',
//         display: 'flex',
//         flexDirection: 'column',
//         bgcolor: 'background.paper',
//         borderRadius: 2,
//         overflow: 'hidden',
//       }}
//     >
//       {/* Header */}
//       <Box sx={{ 
//         p: 2, 
//         bgcolor: 'primary.main', 
//         color: 'white',
//         display: 'flex',
//         alignItems: 'center',
//         gap: 1.5
//       }}>
//         <Avatar sx={{ bgcolor: 'white', color: 'primary.main', width: 32, height: 32 }}>
//           <SendIcon fontSize="small" />
//         </Avatar>
//         <Typography variant="h6" fontWeight={600}>
//           PDF Assistant
//         </Typography>
//       </Box>

//       {/* Messages */}
//       <Box sx={{ 
//         flex: 1, 
//         p: 2, 
//         overflowY: 'auto',
//         bgcolor: 'background.default',
//         '&::-webkit-scrollbar': { width: '6px' },
//         '&::-webkit-scrollbar-track': { background: 'transparent' },
//         '&::-webkit-scrollbar-thumb': { background: '#888', borderRadius: '3px' },
//       }}>
//         {messages.map((msg, idx) => (
//           <Fade in={true} key={idx} timeout={300}>
//             <Box sx={{ 
//               display: 'flex',
//               mb: 2,
//               justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
//             }}>
//               <Box sx={{
//                 p: 2,
//                 borderRadius: 2,
//                 bgcolor: msg.role === 'user' ? 'primary.main' : 'background.paper',
//                 color: msg.role === 'user' ? 'white' : 'text.primary',
//                 boxShadow: 1,
//                 maxWidth: '85%',
//               }}>
//                 <Typography 
//                   variant="body2"
//                   dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br>') }}
//                 />
//                 <Typography variant="caption" sx={{ 
//                   display: 'block',
//                   mt: 0.5,
//                   color: msg.role === 'user' ? 'rgba(255,255,255,0.7)' : 'text.secondary',
//                   textAlign: 'right',
//                   fontSize: '0.7rem'
//                 }}>
//                   {msg.role === 'user' ? 'You' : 'Assistant'}
//                 </Typography>
//               </Box>
//             </Box>
//           </Fade>
//         ))}
//         {isLoading && (
//           <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
//             <Box sx={{
//               p: 2,
//               borderRadius: 2,
//               bgcolor: 'background.paper',
//               boxShadow: 1,
//               display: 'flex',
//               alignItems: 'center',
//               gap: 1
//             }}>
//               <CircularProgress size={16} thickness={5} />
//               <Typography variant="body2">Thinking...</Typography>
//             </Box>
//           </Box>
//         )}
//         <div ref={messagesEndRef} />
//       </Box>

//       {/* Input */}
//       <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider' }}>
//         <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
//           <TextField
//             fullWidth
//             variant="outlined"
//             placeholder="Type your question..."
//             value={query}
//             onChange={(e) => setQuery(e.target.value)}
//             onKeyDown={handleKeyDown}
//             multiline
//             maxRows={4}
//             disabled={isLoading}
//             sx={{
//               '& .MuiOutlinedInput-root': {
//                 borderRadius: 4,
//                 bgcolor: 'background.default',
//                 '&:hover fieldset': { borderColor: 'primary.main' },
//                 '&.Mui-focused fieldset': { borderColor: 'primary.main' },
//               },
//             }}
//           />
//           <Button
//             variant="contained"
//             color="primary"
//             onClick={handleSend}
//             disabled={!query.trim() || isLoading}
//             sx={{ 
//               minWidth: '48px',
//               width: '48px',
//               height: '48px',
//               borderRadius: '50%',
//               p: 0,
//               '&:hover': {
//                 transform: 'scale(1.05)',
//                 transition: 'transform 0.2s',
//               },
//             }}
//           >
//             <SendIcon />
//           </Button>
//         </Box>
//       </Box>
//     </Paper>
//   );
// };

// export default ChatBox;
// import React, { useState, useEffect, useRef } from 'react';
// import { Box, TextField, Button, Typography, Divider, Stack, CircularProgress } from '@mui/material';
// import axios from 'axios';

// const ChatBox = ({ sessionId, fileNames }) => {
//   const [query, setQuery] = useState('');
//   const [messages, setMessages] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const messagesEndRef = useRef(null);

//   // Scroll to the bottom of the chat when new messages are added
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const handleSend = async () => {
//     if (!query.trim() || isLoading) return;

//     const updatedMessages = [...messages, { role: 'user', content: query }];
//     setMessages(updatedMessages);
//     setQuery('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://127.0.0.1:8000/api/chat', {
//         session_id: sessionId,
//         files: fileNames,
//         query: query,
//         history: JSON.stringify(updatedMessages)
//       });

//       const assistantMessage = {
//         role: 'assistant',
//         content: response.data.response || 'No response received'
//       };

//       setMessages([...updatedMessages, assistantMessage]);
//     } catch (err) {
//       console.error('Chat error:', err);
//       setMessages([...updatedMessages, { role: 'assistant', content: 'Failed to send message.' }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e) => {
//     if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   return (
//     <Box
//       sx={{
//         display: 'flex',
//         flexDirection: 'column',
//         height: '100%',
//         bgcolor: '#27292D',
//       }}
//     >
//       {/* Static Header */}
//       <Box sx={{ p: 2 }}>
//         <Typography variant="h3" color="text.primary" sx={{ mb: 2 }}>
//           💬 Chat with the Report
//         </Typography>
//         <Divider sx={{ bgcolor: '#424242' }} />
//       </Box>
//       {/* Scrollable Chat Messages */}
//       <Box
//         sx={{
//           flex: 1,
//           overflowY: 'auto',
//           px: 2,
//           py: 1,
//           '&::-webkit-scrollbar': { width: '8px' },
//           '&::-webkit-scrollbar-thumb': { backgroundColor: '#424242', borderRadius: '4px' },
//           '&::-webkit-scrollbar-track': { backgroundColor: '#27292D' },
//           scrollbarWidth: 'thin',
//           scrollbarColor: '#424242 #27292D',
//         }}
//       >
//         {messages.map((msg, idx) => (
//           <Box
//             key={idx}
//             sx={{
//               display: 'flex',
//               justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
//               mb: 1.5,
//             }}
//           >
//             <Box
//               sx={{
//                 maxWidth: '70%',
//                 p: 1.5,
//                 borderRadius: 3,
//                 bgcolor: msg.role === 'user' ? '#42a5f5' : '#424242',
//                 color: '#ffffff',
//                 wordBreak: 'break-word',
//               }}
//             >
//               <Typography
//                 variant="body1"
//                 dangerouslySetInnerHTML={{ __html: msg.content }}
//               />
//             </Box>
//           </Box>
//         ))}
//         {isLoading && (
//           <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1.5 }}>
//             <CircularProgress size={24} sx={{ color: '#b0bec5' }} />
//           </Box>
//         )}
//         <div ref={messagesEndRef} />
//       </Box>
//       {/* Static Input and Button */}
//       <Box sx={{ p: 2 }}>
//         <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
//           <TextField
//             fullWidth
//             label="Ask a question"
//             value={query}
//             onChange={(e) => setQuery(e.target.value)}
//             onKeyPress={handleKeyPress}
//             variant="outlined"
//             disabled={isLoading}
//             sx={{
//               bgcolor: 'background.paper',
//               borderRadius: 3,
//               '& .MuiOutlinedInput-root': {
//                 borderRadius: 3,
//                 color: '#ffffff',
//                 '& fieldset': { borderColor: '#424242' },
//                 '&:hover fieldset': { borderColor: '#b0bec5' },
//                 '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 '&.Mui-disabled fieldset': { borderColor: '#424242' },
//               },
//               '& .MuiInputBase-input': { color: '#ffffff' },
//               '& .MuiInputLabel-root': { color: '#b0bec5' },
//               '& .MuiInputLabel-root.Mui-focused': { color: '#42a5f5' },
//               '& .MuiInputLabel-root.Mui-disabled': { color: '#b0bec5' },
//             }}
//           />
//           <Button
//             variant="contained"
//             onClick={handleSend}
//             disabled={isLoading || !query.trim()}
//             sx={{
//               borderRadius: 3,
//               bgcolor: '#42a5f5',
//               '&:hover': { bgcolor: '#1e88e5' },
//               '&.Mui-disabled': { bgcolor: '#42a5f5', opacity: 0.5 },
//               textTransform: 'none',
//               height: '40px',
//             }}
//           >
//             Send
//           </Button>
//         </Stack>
//       </Box>
//     </Box>
//   );
// };

// export default ChatBox;


////////////////////////////////////////////////////////////////GROK( friday )//////////////////////////////////////////////////////////////////////////


import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography, Divider, Stack, CircularProgress, Tooltip } from '@mui/material';
import axios from 'axios';

const ChatBox = ({ sessionId, fileNames, selectedFile, pdfBlobs, onCitationClick }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to the bottom of the chat when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const parseCitations = (text) => {
    if (!text || typeof text !== "string") return text;
  
    // Clean unnecessary tags except citation markers
    let cleanedText = text
      .replace(/<sup><span[^>]*>\[(\d+)\][\s\S]*?<\/span><\/sup>/g, "[$1]")
      .replace(/<\/?(div|span|strong|br|p)[^>]*>/g, "");
  
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
          enterDelay={100}
          leaveDelay={200}
          componentsProps={{
            tooltip: {
              sx: {
                fontSize: '1rem',
                maxWidth: 400,
                whiteSpace: 'pre-line',
                bgcolor: '#424242',
                color: '#ffffff',
                padding: '8px',
              },
            },
          }}
        >
          <span
            onClick={async () => {
              try {
                const res = await axios.get('http://127.0.0.1:8000/api/citation-text', {
                  params: {
                    filename: sourceFile,
                    page: parseInt(pageNum),
                    highlight: context
                  }
                });
  
                if (res.data.status === 'success') {
                  onCitationClick({
                    file: sourceFile,
                    page: parseInt(pageNum),
                    blobUrl: pdfBlobs[sourceFile],
                    highlightedPages: res.data.pages,
                    highlightedPage: res.data.highlighted_page
                  });
                } else {
                  console.error('API failed:', res.data.message);
                  alert('Failed to fetch citation text.');
                }
              } catch (error) {
                console.error('Error fetching citation text:', error);
                alert('Error fetching citation text from server.');
              }
            }}
            style={{
              cursor: 'pointer',
              color: '#42a5f5',
              textDecoration: 'underline dotted'
            }}
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
  

  const handleSend = async () => {
    if (!query.trim() || isLoading) return;

    const updatedMessages = [...messages, { role: 'user', content: query }];
    setMessages(updatedMessages);
    setQuery('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/chat', {
        session_id: sessionId,
        files: selectedFile ? [selectedFile] : fileNames,
        query: query,
        history: JSON.stringify(updatedMessages)
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response || 'No response received'
      };

      setMessages([...updatedMessages, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages([...updatedMessages, { role: 'assistant', content: 'Failed to send message.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        bgcolor: '#27292D',
      }}
    >
      {/* Static Header */}
      <Box sx={{ p: 2 }}>
        <Typography variant="h3" color="text.primary" sx={{ mb: 2 }}>
          💬 Chat with the Report
        </Typography>
        <Divider sx={{ bgcolor: '#424242' }} />
      </Box>
      {/* Scrollable Chat Messages */}
      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          px: 2,
          py: 1,
          '&::-webkit-scrollbar': { width: '8px' },
          '&::-webkit-scrollbar-thumb': { backgroundColor: '#424242', borderRadius: '4px' },
          '&::-webkit-scrollbar-track': { backgroundColor: '#27292D' },
          scrollbarWidth: 'thin',
          scrollbarColor: '#424242 #27292D',
        }}
      >
        {messages.map((msg, idx) => (
          <Box
            key={idx}
            sx={{
              display: 'flex',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
              mb: 1.5,
            }}
          >
            <Box
              sx={{
                maxWidth: '70%',
                p: 1.5,
                borderRadius: 3,
                bgcolor: msg.role === 'user' ? '#42a5f5' : '#424242',
                color: '#ffffff',
                wordBreak: 'break-word',
              }}
            >
              <Typography
                variant="body1"
                component="span"
                sx={{ display: 'inline' }}
              >
                {parseCitations(msg.content)}
              </Typography>
            </Box>
          </Box>
        ))}
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1.5 }}>
            <CircularProgress size={24} sx={{ color: '#b0bec5' }} />
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>
      {/* Static Input and Button */}
      <Box sx={{ p: 2 }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
          <TextField
            fullWidth
            label="Ask a question"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            variant="outlined"
            disabled={isLoading}
            sx={{
              bgcolor: 'background.paper',
              borderRadius: 3,
              '& .MuiOutlinedInput-root': {
                borderRadius: 3,
                color: '#ffffff',
                '& fieldset': { borderColor: '#424242' },
                '&:hover fieldset': { borderColor: '#b0bec5' },
                '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                '&.Mui-disabled fieldset': { borderColor: '#424242' },
              },
              '& .MuiInputBase-input': { color: '#ffffff' },
              '& .MuiInputLabel-root': { color: '#b0bec5' },
              '& .MuiInputLabel-root.Mui-focused': { color: '#42a5f5' },
              '& .MuiInputLabel-root.Mui-disabled': { color: '#b0bec5' },
            }}
          />
          <Button
            variant="contained"
            onClick={handleSend}
            disabled={isLoading || !query.trim()}
            sx={{
              borderRadius: 3,
              bgcolor: '#42a5f5',
              '&:hover': { bgcolor: '#1e88e5' },
              '&.Mui-disabled': { bgcolor: '#42a5f5', opacity: 0.5 },
              textTransform: 'none',
              height: '40px',
            }}
          >
            Send
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};

export default ChatBox;




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// import React, { useState, useEffect, useRef } from 'react';
// import { Box, TextField, Button, Typography, Divider, Stack, CircularProgress, Tooltip } from '@mui/material';
// import axios from 'axios';
// import InlinePDFViewer from './inlinePDFviewer'; // ✅ Import the viewer

// const ChatBox = ({ sessionId, fileNames, selectedFile, pdfBlobs }) => {
//   const [query, setQuery] = useState('');
//   const [messages, setMessages] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const messagesEndRef = useRef(null);

//   // ✅ New states for selected citation
//   const [selectedFilename, setSelectedFilename] = useState(null);
//   const [selectedPage, setSelectedPage] = useState(null);
//   const [selectedText, setSelectedText] = useState(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const parseCitations = (text) => {
//     if (!text || typeof text !== "string") return text;

//     const citationRegex = /<sup><span class='citation'[^>]*data-source='([^']+)'[^>]*data-page='([^']+)'[^>]*data-context='([^']*)'[^>]*>\[(\d+)\]/g;

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
//         >
//           <span
//             onClick={() => {
//               setSelectedFilename(sourceFile);
//               setSelectedPage(parseInt(pageNum));
//               setSelectedText(context);
//             }}
//             style={{
//               cursor: 'pointer',
//               color: '#42a5f5',
//               textDecoration: 'underline dotted'
//             }}
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

//   const handleSend = async () => {
//     if (!query.trim() || isLoading) return;

//     const updatedMessages = [...messages, { role: 'user', content: query }];
//     setMessages(updatedMessages);
//     setQuery('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://127.0.0.1:8000/api/chat', {
//         session_id: sessionId,
//         files: selectedFile ? [selectedFile] : fileNames,
//         query: query,
//         history: JSON.stringify(updatedMessages)
//       });

//       const assistantMessage = {
//         role: 'assistant',
//         content: response.data.response || 'No response received'
//       };

//       setMessages([...updatedMessages, assistantMessage]);
//     } catch (err) {
//       console.error('Chat error:', err);
//       setMessages([...updatedMessages, { role: 'assistant', content: 'Failed to send message.' }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e) => {
//     if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   return (
//     <>
//       {/* ✅ Show PDF viewer if a citation is selected */}
//       {selectedFilename && (
//         <InlinePDFViewer
//           filename={selectedFilename}
//           page={selectedPage}
//           highlight={selectedText}
//         />
//       )}

//       <Box
//         sx={{
//           display: 'flex',
//           flexDirection: 'column',
//           height: '100%',
//           bgcolor: '#27292D',
//         }}
//       >
//         {/* Static Header */}
//         <Box sx={{ p: 2 }}>
//           <Typography variant="h3" color="text.primary" sx={{ mb: 2 }}>
//             💬 Chat with the Report
//           </Typography>
//           <Divider sx={{ bgcolor: '#424242' }} />
//         </Box>

//         {/* Scrollable Chat Messages */}
//         <Box
//           sx={{
//             flex: 1,
//             overflowY: 'auto',
//             px: 2,
//             py: 1,
//             '&::-webkit-scrollbar': { width: '8px' },
//             '&::-webkit-scrollbar-thumb': { backgroundColor: '#424242', borderRadius: '4px' },
//             '&::-webkit-scrollbar-track': { backgroundColor: '#27292D' },
//             scrollbarWidth: 'thin',
//             scrollbarColor: '#424242 #27292D',
//           }}
//         >
//           {messages.map((msg, idx) => (
//             <Box
//               key={idx}
//               sx={{
//                 display: 'flex',
//                 justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
//                 mb: 1.5,
//               }}
//             >
//               <Box
//                 sx={{
//                   maxWidth: '70%',
//                   p: 1.5,
//                   borderRadius: 3,
//                   bgcolor: msg.role === 'user' ? '#42a5f5' : '#424242',
//                   color: '#ffffff',
//                   wordBreak: 'break-word',
//                 }}
//               >
//                 <Typography variant="body1" component="span" sx={{ display: 'inline' }}>
//                   {parseCitations(msg.content)}
//                 </Typography>
//               </Box>
//             </Box>
//           ))}
//           {isLoading && (
//             <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1.5 }}>
//               <CircularProgress size={24} sx={{ color: '#b0bec5' }} />
//             </Box>
//           )}
//           <div ref={messagesEndRef} />
//         </Box>

//         {/* Input and Send Button */}
//         <Box sx={{ p: 2 }}>
//           <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
//             <TextField
//               fullWidth
//               label="Ask a question"
//               value={query}
//               onChange={(e) => setQuery(e.target.value)}
//               onKeyPress={handleKeyPress}
//               variant="outlined"
//               disabled={isLoading}
//               sx={{
//                 bgcolor: 'background.paper',
//                 borderRadius: 3,
//                 '& .MuiOutlinedInput-root': {
//                   borderRadius: 3,
//                   color: '#ffffff',
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                   '&.Mui-disabled fieldset': { borderColor: '#424242' },
//                 },
//                 '& .MuiInputBase-input': { color: '#ffffff' },
//                 '& .MuiInputLabel-root': { color: '#b0bec5' },
//                 '& .MuiInputLabel-root.Mui-focused': { color: '#42a5f5' },
//                 '& .MuiInputLabel-root.Mui-disabled': { color: '#b0bec5' },
//               }}
//             />
//             <Button
//               variant="contained"
//               onClick={handleSend}
//               disabled={isLoading || !query.trim()}
//               sx={{
//                 borderRadius: 3,
//                 bgcolor: '#42a5f5',
//                 '&:hover': { bgcolor: '#1e88e5' },
//                 '&.Mui-disabled': { bgcolor: '#42a5f5', opacity: 0.5 },
//                 textTransform: 'none',
//                 height: '40px',
//               }}
//             >
//               Send
//             </Button>
//           </Stack>
//         </Box>
//       </Box>
//     </>
//   );
// };

// export default ChatBox;
