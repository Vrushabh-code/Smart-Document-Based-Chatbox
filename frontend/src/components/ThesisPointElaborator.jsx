// import React, { useState } from 'react';
// import axios from 'axios';
// import { Box, Typography, TextField, Button, Alert, CircularProgress } from '@mui/material';

// const ThesisPointElaborator = ({ onError }) => {
//   const [point, setPoint] = useState('');
//   const [wordCount, setWordCount] = useState(200);
//   const [detailedPoint, setDetailedPoint] = useState(null);
//   const [elaborating, setElaborating] = useState(false);
//   const [success, setSuccess] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!point) {
//       onError('Please provide a thesis point to elaborate.');
//       return;
//     }

//     setElaborating(true);
//     try {
//       const response = await axios.post('http://localhost:8000/api/elaborate-thesis-point', {
//         point,
//         word_count: wordCount,
//       });
//       setDetailedPoint(response.data.detailed_point);
//       setSuccess('Thesis point elaborated successfully.');
//     } catch (error) {
//       onError(error.response?.data?.detail || 'Error elaborating thesis point.');
//     } finally {
//       setElaborating(false);
//     }
//   };

//   return (
//     <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
//       <Typography variant="h3" gutterBottom color="text.primary">
//         Elaborate Thesis Point
//       </Typography>
//       {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
//       <form onSubmit={handleSubmit}>
//         <TextField
//           fullWidth
//           multiline
//           rows={4}
//           label="Thesis Point"
//           value={point}
//           onChange={(e) => setPoint(e.target.value)}
//           placeholder="Enter thesis point to elaborate"
//           sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
//         />
//         <TextField
//           fullWidth
//           type="number"
//           label="Word Count"
//           value={wordCount}
//           onChange={(e) => setWordCount(parseInt(e.target.value))}
//           inputProps={{ min: 100, max: 1000 }}
//           sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
//         />
//         <Button
//           type="submit"
//           variant="contained"
//           color="secondary"
//           disabled={elaborating}
//           startIcon={elaborating ? <CircularProgress size={20} /> : null}
//         >
//           {elaborating ? 'Elaborating...' : 'Elaborate Point'}
//         </Button>
//       </form>
//       {detailedPoint && (
//         <Box sx={{ mt: 2, p: 2, bgcolor: '#27292D' }}>
//           <Typography variant="h6" color="text.primary">Detailed Point</Typography>
//           <Typography component="div" color="text.secondary" dangerouslySetInnerHTML={{ __html: detailedPoint }} />
//         </Box>
//       )}
//     </Box>
//   );
// };

// export default ThesisPointElaborator;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import React, { useState } from 'react';
import axios from 'axios';
import { Box, Typography, TextField, Button, Alert, CircularProgress } from '@mui/material';

const ThesisPointElaborator = ({ onError }) => {
  const [point, setPoint] = useState('');
  const [wordCount, setWordCount] = useState(200);
  const [detailedPoint, setDetailedPoint] = useState(null);
  const [elaborating, setElaborating] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!point) {
      onError('Please provide a thesis point to elaborate.');
      return;
    }

    setElaborating(true);
    try {
      const response = await axios.post('http://localhost:8000/api/elaborate-thesis-point', {
        point,
        word_count: wordCount,
      });
      setDetailedPoint(response.data.detailed_point);
      setSuccess('Thesis point elaborated successfully.');
    } catch (error) {
      onError(error.response?.data?.detail || 'Error elaborating thesis point.');
    } finally {
      setElaborating(false);
    }
  };

  return (
    <Box sx={{ mb: 1.5, bgcolor: '#27292D', p: 1.5 }} // Reduced mb: 2 to 1.5, p: 2 to 1.5
    >
      <Typography variant="h3" gutterBottom color="text.primary" sx={{ fontSize: '1.5rem' }} // Added fontSize: 1.5rem
      >
        Elaborate Thesis Point
      </Typography>
      {success && <Alert severity="success" sx={{ mb: 1.5 }} // Reduced mb: 2 to 1.5
      >{success}</Alert>}
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          multiline
          rows={3} // Reduced from 4 to 3 (0.75 * 4)
          label="Thesis Point"
          value={point}
          onChange={(e) => setPoint(e.target.value)}
          placeholder="Enter thesis point to elaborate"
          sx={{ mb: 1.5, bgcolor: 'background.paper', borderRadius: 1 }} // Reduced mb: 2 to 1.5
        />
        <TextField
          fullWidth
          type="number"
          label="Word Count"
          value={wordCount}
          onChange={(e) => setWordCount(parseInt(e.target.value))}
          inputProps={{ min: 100, max: 1000 }}
          sx={{ mb: 1.5, bgcolor: 'background.paper', borderRadius: 1 }} // Reduced mb: 2 to 1.5
        />
        <Button
          type="submit"
          variant="contained"
          color="secondary"
          disabled={elaborating}
          startIcon={elaborating ? <CircularProgress size={15} /> : null} // Reduced size: 20 to 15 (0.75 * 20)
          sx={{ fontSize: '0.75rem', py: 0.75, px: 1.5 }} // Added fontSize, py, px
        >
          {elaborating ? 'Elaborating...' : 'Elaborate Point'}
        </Button>
      </form>
      {detailedPoint && (
        <Box sx={{ mt: 1.5, p: 1.5, bgcolor: '#27292D' }} // Reduced mt: 2 to 1.5, p: 2 to 1.5
        >
          <Typography variant="h6" color="text.primary" sx={{ fontSize: '0.9375rem' }} // Added fontSize: 0.9375rem (0.75 * ~1.25rem)
          >Detailed Point</Typography>
          <Typography component="div" color="text.secondary" dangerouslySetInnerHTML={{ __html: detailedPoint }} />
        </Box>
      )}
    </Box>
  );
};

export default ThesisPointElaborator;