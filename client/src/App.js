import { Box, Container, Button, FormControl, FormHelperText, Input, InputLabel, Grow } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function App() {
    const navigate = useNavigate()
    
    const handleSubmit = (e) => {
        e && e.preventDefault();
        if (e.target.query.value === "") { 
            alert("Please entre your query to continue")
        }
        else {
            navigate(`/search/${e.target.query.value}`)
        }
    }

    return (
        <Container sx={{ height: "100%", width: "100%", display: "flex", justifyContent: "center" }}>
            <Box className="content" display="flex" justifyContent="center">
                <h2>121 Search</h2>
                <h2>121 Search</h2>
            </Box>
            <Grow in timeout={800}>
                <Box
                    component="form"
                    onSubmit={handleSubmit}
                    noValidate
                    autoComplete="off"
                    display="flex"
                    alignItems="center"
                >
                    <FormControl>
                        <InputLabel>Search Query:</InputLabel>
                        <Input name="query" aria-describedby="help-text" />
                        <FormHelperText id="help-text">Please Input Your Query</FormHelperText>
                    </FormControl>
                    <FormControl>
                        <Button sx={{ ml: "1rem" }} type="submit" variant="contained">GO</Button>
                    </FormControl>
                </Box>
            </Grow>
        </Container>
    );
}

export default App;
