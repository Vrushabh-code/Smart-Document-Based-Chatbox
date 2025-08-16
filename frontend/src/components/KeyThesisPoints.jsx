// import React, { useState } from 'react';
// import {
//   Card,
//   Typography,
//   Box,
//   Button,
//   TextField,
//   Stack
// } from '@mui/material';
// import axios from 'axios';

// const KeyThesisPoints = ({ keyThesisPoints = [], taskId, onUpdate }) => {
//   const [wordCount, setWordCount] = useState(50); // default word count step

//   const [newPrompt, setNewPrompt] = useState('');
// const [elaboratedPoint, setElaboratedPoint] = useState(null);
// const [adding, setAdding] = useState(false);

//   const handleAdjustLength = async (index, direction) => {
//     if (!newPrompt || !wordCount) return;

//     setAdding(true);
//     try {
//       await axios.post(`http://127.0.0.1:8000/api/add-thesis-point/${taskId}`, {
//         prompt: newPrompt,
//         word_count: wordCount
//       });
  
//       const response = await axios.post(`http://127.0.0.1:8000/api/elaborate-thesis-point/${taskId}`, {
//         point: newPrompt,
//         word_count: wordCount
//       });
  
//       setElaboratedPoint(response.data?.detailed_point || null);
  
//       if (onUpdate && response.data?.key_thesis_points) {
//         onUpdate(response.data.key_thesis_points);
//       }
//     } catch (err) {
//       console.error("Error adding/elaborating:", err);
//       alert("Failed to add/elaborate thesis point.");
//     } finally {
//       setAdding(false);
//     }
//   };

//   return (
//     <Box className="section-card">
//       <Typography variant="h3" gutterBottom>
//         Key Thesis Points
//       </Typography>

//       {/* Word count step input */}
//       <TextField
//         label="Word Count Step"
//         type="number"
//         value={wordCount}
//         onChange={(e) => setWordCount(parseInt(e.target.value) || 0)}
//         size="small"
//         sx={{ mb: 2 }}
//       />
//       <TextField
//   label="New Thesis Prompt"
//   fullWidth
//   value={newPrompt}
//   onChange={(e) => setNewPrompt(e.target.value)}
//   placeholder="Enter new key thesis point prompt"
//   multiline
//   rows={3}
//   sx={{ mb: 2 }}
// />
// <Button
//   variant="contained"
//   color="primary"
//   onClick={handleAddAndElaborate}
//   disabled={adding || !newPrompt}
//   sx={{ mb: 2 }}
// >
//   {adding ? 'Adding...' : 'Add Thesis Point'}
// </Button>


//       <Card>
//         <Box p={2}>
//           {keyThesisPoints.length > 0 ? (
//             <ul>
//               {keyThesisPoints.map((point, index) => (
//                 <li key={index}>
//                   <Typography paragraph>{point}</Typography>

//                   <Stack direction="row" spacing={1} mb={2}>
//                     <Button
//                       size="small"
//                       variant="outlined"
//                       onClick={() => handleAdjustLength(index, 'increase')}
//                     >
//                       Increase
//                     </Button>
//                     <Button
//                       size="small"
//                       variant="outlined"
//                       onClick={() => handleAdjustLength(index, 'decrease')}
//                     >
//                       Decrease
//                     </Button>
//                   </Stack>
//                 </li>
//               ))}
//             </ul>
//           ) : (
//             <Typography>No key thesis points available.</Typography>
//           )}
//         </Box>
//       </Card>
//       {elaboratedPoint && (
//   <Card sx={{ mt: 2 }}>
//     <Box p={2}>
//       <Typography variant="h6">Elaborated Point</Typography>
//       <Typography component="div" dangerouslySetInnerHTML={{ __html: elaboratedPoint }} />
//     </Box>
//   </Card>
// )}
//     </Box>
//   );
// };

// export default KeyThesisPoints;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// import React, { useState } from 'react';
// import {
//   Card,
//   Typography,
//   Box,
//   Button,
//   TextField,
//   Stack,
//   CircularProgress,
// } from '@mui/material';
// import axios from 'axios';

// const KeyThesisPoints = ({ keyThesisPoints = [], taskId, onUpdate }) => {
//   const defaultWordCount = 200;
//   const [wordCounts, setWordCounts] = useState({});
//   const [elaboratedPoints, setElaboratedPoints] = useState({});
//   const [loadingIndex, setLoadingIndex] = useState(null);

//   const handleAdjustLength = async (index, direction) => {
//     try {
//       const wordCount = wordCounts[index] || defaultWordCount;

//       const response = await axios.post(`http://127.0.0.1:8000/api/adjust-thesis-length/${taskId}`, {
//         index,
//         direction,
//         word_count: wordCount,
//       });

//       if (response.data?.key_thesis_points && onUpdate) {
//         onUpdate(response.data.key_thesis_points);
//       }
//     } catch (error) {
//       console.error("Error adjusting thesis point:", error);
//       alert("Failed to adjust thesis point.");
//     }
//   };

//   const handleElaborate = async (index, point) => {
//     const wordCount = wordCounts[index] || defaultWordCount;
//     setLoadingIndex(index);

//     try {
//       const response = await axios.post(
//         `http://127.0.0.1:8000/api/elaborate-thesis-point/${taskId}`,
//         {
//           point,
//           word_count: wordCount,
//         }
//       );

//       setElaboratedPoints((prev) => ({
//         ...prev,
//         [index]: response.data?.detailed_point || 'No elaboration returned.',
//       }));
//     } catch (err) {
//       console.error('Error elaborating thesis point:', err);
//       alert('Failed to elaborate thesis point.');
//     } finally {
//       setLoadingIndex(null);
//     }
//   };

//   const handleWordCountChange = (index, value) => {
//     setWordCounts((prev) => ({
//       ...prev,
//       [index]: parseInt(value) || 0,
//     }));
//   };

//   return (
//     <Box className="section-card">
//       <Typography variant="h3" gutterBottom>
//         Key Thesis Points
//       </Typography>

//       <Card>
//         <Box p={2}>
//           {keyThesisPoints.length === 0 ? (
//             <Typography>No key thesis points available.</Typography>
//           ) : (
//             <ul>
//               {keyThesisPoints.map((point, index) => (
//                 <li key={index} style={{ marginBottom: '1.5rem' }}>
//                   <Typography paragraph>{point}</Typography>

//                   <Stack direction="row" spacing={1} alignItems="center" mb={1}>
//                     <TextField
//                       label="Word Count"
//                       type="number"
//                       size="small"
//                       value={wordCounts[index] || defaultWordCount}
//                       onChange={(e) => handleWordCountChange(index, e.target.value)}
//                       sx={{ width: 120 }}
//                     />

//                     <Button
//                       variant="outlined"
//                       size="small"
//                       onClick={() => handleAdjustLength(index, 'increase')}
//                     >
//                       Increase
//                     </Button>

//                     <Button
//                       variant="outlined"
//                       size="small"
//                       onClick={() => handleAdjustLength(index, 'decrease')}
//                     >
//                       Decrease
//                     </Button>

//                     <Button
//                       variant="contained"
//                       size="small"
//                       onClick={() => handleElaborate(index, point)}
//                       disabled={loadingIndex === index}
//                     >
//                       {loadingIndex === index ? <CircularProgress size={16} /> : 'Add'}
//                     </Button>
//                   </Stack>

//                   {elaboratedPoints[index] && (
//                     <Box
//                       sx={{
//                         backgroundColor: '#f9f9f9',
//                         borderLeft: '4px solid #1976D2',
//                         padding: 2,
//                         borderRadius: 1,
//                         mt: 1,
//                       }}
//                     >
//                       <Typography variant="subtitle1" gutterBottom>
//                         Elaborated Point
//                       </Typography>
//                       <Typography
//                         component="div"
//                         dangerouslySetInnerHTML={{ __html: elaboratedPoints[index] }}
//                       />
//                     </Box>
//                   )}
//                 </li>
//               ))}
//             </ul>
//           )}
//         </Box>
//       </Card>
//     </Box>
//   );
// };

// export default KeyThesisPoints;


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// import React, { useState } from 'react';
// import {
//   Typography,
//   Box,
//   Button,
//   Stack,
//   CircularProgress
// } from '@mui/material';
// import axios from 'axios';

// const KeyThesisPoints = ({ keyThesisPoints = [], taskId, onUpdate }) => {
//   console.log("Received taskId:", taskId);
//   const defaultWordCount = 150;
//   const [elaboratedPoints, setElaboratedPoints] = useState({});
//   const [loadingIndex, setLoadingIndex] = useState(null);
//   const [addingIndex, setAddingIndex] = useState(null);

//   const handleElaborate = async (index, point) => {
//     setLoadingIndex(index);
  
//     try {
//       const response = await axios.post(
//         `http://127.0.0.1:8000/api/add-thesis-point/${taskId}`,
//         {
//           prompt: point,
//           word_count: defaultWordCount,
//         }
//       );
  
//       setElaboratedPoints((prev) => ({
//         ...prev,
//         [index]: response.data?.elaborated_text || 'No elaboration returned.',
//       }));
//     } catch (err) {
//       console.error('Error elaborating thesis point:', err);
//       alert('Failed to elaborate thesis point.');
//     } finally {
//       setLoadingIndex(null);
//     }
//   };

//   return (
//     <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
//       <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
//         Key Thesis Points
//       </Typography>
//       {keyThesisPoints.length === 0 ? (
//         <Typography color="text.secondary">No key thesis points available.</Typography>
//       ) : (
//         <ul style={{ paddingLeft: 0 }}>
//           {keyThesisPoints.map((point, index) => (
//             <li key={index} style={{ marginBottom: '2rem', listStyle: 'none' }}>
//               <Typography paragraph color="text.secondary">{point}</Typography>
//               <Stack direction="row" spacing={1} mb={1}>
//                 {!elaboratedPoints[index] && (
//                   <Button
//                     variant="contained"
//                     size="small"
//                     onClick={() => handleElaborate(index, point)}
//                     disabled={loadingIndex === index}
//                     sx={{
//                       mr: 1,
//                       whiteSpace: 'nowrap',
//                       minWidth: 'auto',
//                       height: '36px',
//                       padding: '6px 16px',
//                       alignSelf: 'flex-start'
//                     }}
//                   >
//                     {loadingIndex === index ? <CircularProgress size={16} /> : 'ADD'}
//                   </Button>
//                 )}
//                 {elaboratedPoints[index] && (
//                   <Box
//                     sx={{
//                       backgroundColor: '#27292D',
//                       borderLeft: '4px solid',
//                       borderColor: 'primary.main',
//                       padding: 2,
//                       borderRadius: 2,
//                       mt: 2,
//                     }}
//                   >
//                     <Typography variant="subtitle1" gutterBottom color="text.primary">
//                       Elaborated Point
//                     </Typography>
//                     <Typography
//                       component="div"
//                       color="text.secondary"
//                       dangerouslySetInnerHTML={{ __html: elaboratedPoints[index] }}
//                     />
//                     <Typography variant="caption" color="success.main" sx={{ mt: 1 }}>
//                       ✅ Added & elaborated successfully.
//                     </Typography>
//                   </Box>
//                 )}
//               </Stack>
//             </li>
//           ))}
//         </ul>
//       )}
//     </Box>
//   );
// };

// export default KeyThesisPoints;




///////////////////////////////////////////////////////////////GROK(friday)////////////////////////////////////////////////////////


import React, { useState } from 'react';
import { Box, Typography, Button, List, ListItem, ListItemText } from '@mui/material';
import ThesisPointElaborator from './ThesisPointElaborator';

const KeyThesisPoints = ({ keyThesisPoints, taskId, onUpdate }) => {
  const [showElaborator, setShowElaborator] = useState(false);

  const handleElaborate = async (point) => {
    // Assuming elaboration is handled elsewhere or via a prop
  };

  return (
    <Box sx={{ p: 1.5 }} // Reduced p: 2 to 1.5
    >
      <Typography variant="h3" gutterBottom sx={{ fontSize: '1.5rem' }} // Added fontSize: 1.5rem
      >
        Key Thesis Points
      </Typography>
      <List>
        {keyThesisPoints.map((point, index) => (
          <ListItem key={index} sx={{ py: 0.375 }} // Reduced py: 0.5 to 0.375 (0.75 * 0.5)
          >
            <ListItemText
              primary={point}
              primaryTypographyProps={{ fontSize: '0.75rem' }} // Added fontSize: 0.75rem (0.75 * ~1rem)
            />
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleElaborate(point)}
              sx={{ fontSize: '0.75rem', py: 0.75, px: 1.5 }} // Added fontSize, py, px
            >
              Elaborate
            </Button>
          </ListItem>
        ))}
      </List>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => setShowElaborator(!showElaborator)}
        sx={{ mt: 1.5, fontSize: '0.75rem', py: 0.75, px: 1.5 }} // Reduced mt: 2 to 1.5, added fontSize, py, px
      >
        {showElaborator ? 'Hide Elaborator' : 'Add Thesis Point'}
      </Button>
      {showElaborator && (
        <ThesisPointElaborator
          taskId={taskId}
          onUpdate={onUpdate}
        />
      )}
    </Box>
  );
};

export default KeyThesisPoints;