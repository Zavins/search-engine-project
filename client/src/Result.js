import { List, ListItem, Typography, Paper, Container, ListItemButton, CircularProgress, Alert, Link, Box, Button, FormControl, FormHelperText, Input, InputLabel } from "@mui/material"
import axios from "axios"
import { useQuery } from "react-query"
import { useNavigate, useParams } from "react-router-dom"

const Result = () => {
    let { query } = useParams()
    const navigate = useNavigate()

    let { isLoading: loading, error: error, data: data, } = useQuery(
        ["get-result", query],
        async () => {
            let r = await axios.get(`/s/${query}`)
            return r.data
        },
        {
            retry: false
        }
    )

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
            {
                loading === true ? (
                    <CircularProgress disableShrink />
                ) : data[0].length === 0 ? (
                    <Alert severity="error">NO result</Alert>
                ) : (
                    <>
                        <List component={Paper} sx={{ width: '100%', my: "1rem" }}>
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
                            {
                                data[0].map((url) => (
                                    <ListItem alignItems="flex-start" style={{ width: "100%" }}>
                                        <Paper elevation={1} style={{ width: "100%" }} square={true}>
                                            <ListItemButton component={Link} href={url} target="_blank" style={{ padding: "1rem" }}>
                                                <Typography>{url}</Typography>
                                            </ListItemButton>
                                        </Paper>
                                    </ListItem>
                                ))
                            }
                        </List>
                        Time Used: {data[1]}
                    </>
                )
            }
        </Container>
    )
}

export default Result