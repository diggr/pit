import React from 'react'

import { withStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

const styles = theme => ({

})

const OrgAgentProfile = (props) => {
    const { org }  = props

    return (
        <Grid container>
            <Grid item xs={2} >
                <Typography variant="caption" gutterBottom>URI</Typography>
            </Grid>
            <Grid item xs={10} >
                <Typography gutterBottom>{ org.uri }</Typography>
            </Grid>

            <Grid item xs={2} >
                <Typography variant="caption" gutterBottom>Name</Typography>
            </Grid>
            <Grid item xs={10} >
                <Typography component={'span'} gutterBottom>{ org.name.map( (item, i) => <div key={'orgname'+i }>{item}<br /></div> ) }</Typography>
            </Grid>

            <Grid item xs={2} >
                <Typography variant="caption" gutterBottom>Website</Typography>
            </Grid>
            <Grid item xs={10} >
                <Typography gutterBottom><a href={ org.homepage } target="_blank"  rel="noopener noreferrer">{ org.homepage }</a></Typography>
            </Grid>

        </Grid>
    )
}

export default withStyles(styles) (OrgAgentProfile)
