import React from 'react'

import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'


const PersonAgentProfile = (props) => {
    const { person }  = props

    return (
        <Grid container>

            <Grid item xs={2}>
                <Typography variant="caption" gutterBottom>URI</Typography>
            </Grid>
            <Grid item xs={10}>
                <Typography gutterBottom>{ person.uri }</Typography>
            </Grid>

            <Grid item xs={2}>
                <Typography variant="caption" gutterBottom>Name</Typography>
            </Grid>
            <Grid item xs={10}>
                <Typography component={'span'} gutterBottom>
                    { person.name.map( (item, i) => <div key={ 'pname'+i } >{item}<br /></div> ) }
                </Typography>
            </Grid>
 
            <Grid item xs={2}>
                <Typography variant="caption" gutterBottom>Institution</Typography>
            </Grid>
            <Grid item xs={10}>
                <Typography  component={'span'} gutterBottom>
                    { person.institution.map( (item, i) => <div key={ 'pinstitution'+i } >{item}<br /></div> ) }
                </Typography>
            </Grid>

            <Grid item  xs={2}>
                <Typography variant="caption" gutterBottom>Email</Typography>
            </Grid>
            <Grid item xs={10}>
                <Typography  component={'span'} gutterBottom>
                    { person.email.map( (item, i) => <div key={ 'pemail'+i } >{item}<br /></div> ) }
                </Typography>
            </Grid>

            <Grid item xs={2}>
                <Typography variant="caption" gutterBottom>Homepage</Typography>
            </Grid>
            <Grid item xs={10}>
                <Typography  component={'span'} gutterBottom>
                    { person.homepage.map( (item, i) => <div key={ 'phomepage'+i } ><a href={item} target="_new"  rel="noopener noreferrer">{item}</a><br /></div> ) }
                </Typography>
            </Grid>

        </Grid>
    )
}

export default PersonAgentProfile
