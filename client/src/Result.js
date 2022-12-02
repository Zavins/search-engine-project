import { List, ListItem, ListItemAvatar, Avatar, ListItemText, Typography, Divider, Card, Paper, Container, ListItemButton, CircularProgress, Alert, Link } from "@mui/material"
import axios from "axios"
import React from "react"
import { useQuery } from "react-query"
import { useParams } from "react-router-dom"

const Result = () => {
    let { query } = useParams()

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

    console.log(data)

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
                        {data[1]}
                    </>
                )
            }
        </Container>
    )
}

export default Result