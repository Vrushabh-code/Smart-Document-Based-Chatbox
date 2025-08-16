// import React, { useState } from 'react';
// import axios from 'axios';
// import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, CircularProgress } from '@mui/material';

// const ModifySection = ({ onReportGenerated, onError, taskId }) => {
//   const [section, setSection] = useState('business overview');
//   const [prompt, setPrompt] = useState('');
//   const [modifying, setModifying] = useState(false);
//   const [success, setSuccess] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!prompt) {
//       onError('Please provide a modification prompt.');
//       return;
//     }

//     setModifying(true);
//     try {
//       const response = await axios.post(`http://localhost:8000/api/modify-report/${taskId}`, {
//         section,
//         user_prompt: prompt, // ✅ correct key expected by backend
//       });
//       onReportGenerated(response.data);
//       setSuccess('Section modified successfully.');
//     } catch (error) {
//       onError(error.response?.data?.detail || 'Error modifying section.');
//     } finally {
//       setModifying(false);
//     }
//   };

//   return (
//     <Box className="section-card">
//       <Typography variant="h3" gutterBottom>
//         Modify Report Section
//       </Typography>
//       {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
//       <form onSubmit={handleSubmit}>
//         <FormControl fullWidth sx={{ mb: 2 }}>
//           <InputLabel>Section to Modify</InputLabel>
//           <Select
//             value={section}
//             onChange={(e) => setSection(e.target.value)}
//             label="Section to Modify"
//           >
//             <MenuItem value="business overview">Business Overview</MenuItem>
//             <MenuItem value="quarterly earnings">Quarterly Earnings</MenuItem>
//             <MenuItem value="investment thesis">Investment Thesis</MenuItem>
//           </Select>
//         </FormControl>
//         <TextField
//           fullWidth
//           multiline
//           rows={4}
//           label="Modification Prompt"
//           value={prompt}
//           onChange={(e) => setPrompt(e.target.value)}
//           placeholder="Enter modification prompt (e.g., 'Shorten the business overview to 100 words')"
//           sx={{ mb: 2 }}
//         />
//         <Button
//           type="submit"
//           variant="contained"
//           color="secondary"
//           disabled={modifying}
//           startIcon={modifying ? <CircularProgress size={20} /> : null}
//         >
//           {modifying ? 'Modifying...' : 'Modify Section'}
//         </Button>
//       </form>
//     </Box>
//   );
// };

// export default ModifySection;


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////for localstorage///////////////////////////////////////////////////////////////////////

// import React, { useState } from 'react';
// import {
//   Box,
//   Typography,
//   TextField,
//   MenuItem,
//   Button,
//   CircularProgress,
//   Alert
// } from '@mui/material';
// import axios from 'axios';

// const ModifySection = ({ taskId, onReportGenerated }) => {
//   const [selectedSection, setSelectedSection] = useState('');
//   const [userPrompt, setUserPrompt] = useState('');
//   const [loading, setLoading] = useState(false);
//   const [successMessage, setSuccessMessage] = useState('');

//   const handleModify = async () => {
//     if (!selectedSection || !userPrompt) {
//       alert('Please select a section and enter a prompt.');
//       return;
//     }

//     setLoading(true);

//     console.log("🧾 Modifying section:", selectedSection);

//     try {
//       const response = await axios.post(`http://localhost:8000/api/modify-report/${taskId}`, {
//         section: selectedSection,
//         user_prompt: userPrompt,
//       });

//       setSuccessMessage(`✅ Updated ${selectedSection} successfully.`);
//       setUserPrompt('');
//       onReportGenerated((prev) => ({
//         ...prev,
//         [selectedSection.toLowerCase().replace(/ /g, "_")]: response.data.modified_text,
//         key_thesis_points: response.data.key_thesis_points || prev.key_thesis_points,
//         pdf_base64: response.data.pdf_base64 || prev.pdf_base64,
//         task_id: taskId,
//       }));
//     } catch (error) {
//       console.error('Modify Error:', error);
//       alert(error.response?.data?.detail || '❌ Failed to modify section.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
//       <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
//         Modify Report Section
//       </Typography>
//       <TextField
//         select
//         label="Select Section"
//         value={selectedSection}
//         onChange={(e) => setSelectedSection(e.target.value)}
//         fullWidth
//         sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
//       >
//         <MenuItem value="Business Overview">Business Overview</MenuItem>
//         <MenuItem value="Quarterly Highlights">Quarterly Highlights</MenuItem>
//         <MenuItem value="Investment Thesis">Investment Thesis</MenuItem>
//       </TextField>
//       <TextField
//         label="Add Content"
//         multiline
//         rows={4}
//         value={userPrompt}
//         onChange={(e) => setUserPrompt(e.target.value)}
//         placeholder="Enter what you'd like to add"
//         fullWidth
//         sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
//       />
//       <Button
//         variant="contained"
//         color="primary"
//         onClick={handleModify}
//         disabled={loading}
//         sx={{ mb: 2 }}
//       >
//         {loading ? <CircularProgress size={20} /> : 'Submit Update'}
//       </Button>
//       {successMessage && (
//         <Alert severity="success" sx={{ mt: 2 }}>
//           {successMessage}
//         </Alert>
//       )}
//     </Box>
//   );
// };

// export default ModifySection;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  MenuItem,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';

const ModifySection = ({ taskId, onReportGenerated }) => {
  const [selectedSection, setSelectedSection] = useState('');
  const [userPrompt, setUserPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleModify = async () => {
    if (!selectedSection || !userPrompt) {
      alert('Please select a section and enter a prompt.');
      return;
    }

    setLoading(true);

    console.log("🧾 Modifying section:", selectedSection);

    try {
      const response = await axios.post(`http://localhost:8000/api/modify-report/${taskId}`, {
        section: selectedSection,
        user_prompt: userPrompt,
      });

      setSuccessMessage(`✅ Updated ${selectedSection} successfully.`);
      setUserPrompt('');
      onReportGenerated((prev) => ({
        ...prev,
        [selectedSection.toLowerCase().replace(/ /g, "_")]: response.data.modified_text,
        key_thesis_points: response.data.key_thesis_points || prev.key_thesis_points,
        pdf_base64: response.data.pdf_base64 || prev.pdf_base64,
        task_id: taskId,
      }));
    } catch (error) {
      console.error('Modify Error:', error);
      alert(error.response?.data?.detail || '❌ Failed to modify section.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
      <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
        Modify Report Section
      </Typography>
      <TextField
        select
        label="Select Section"
        value={selectedSection}
        onChange={(e) => setSelectedSection(e.target.value)}
        fullWidth
        sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 3, height: '40px' }}
      >
        <MenuItem value="Business Overview">Business Overview</MenuItem>
        <MenuItem value="Quarterly Highlights">Quarterly Highlights</MenuItem>
        <MenuItem value="Investment Thesis">Investment Thesis</MenuItem>
      </TextField>
      <TextField
        label="Add Content"
        multiline
        rows={4}
        value={userPrompt}
        onChange={(e) => setUserPrompt(e.target.value)}
        placeholder="Enter what you'd like to add"
        fullWidth
        sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 3, minHeight: '80px' }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleModify}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? <CircularProgress size={20} /> : 'Submit Update'}
      </Button>
      {successMessage && (
        <Alert severity="success" sx={{ mt: 2 }}>
          {successMessage}
        </Alert>
      )}
    </Box>
  );
};

export default ModifySection;





