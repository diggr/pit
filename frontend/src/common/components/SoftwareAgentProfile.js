import React from 'react'

import { withStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

const styles = theme => ({

})

const PersonAgentProfile = (props) => {
    const { sw }  = props

    return (
        <Grid container>
            <Grid container>
                <Grid item xs={2} >
                    <Typography variant="caption" gutterBottom>URI</Typography>
                </Grid>
                <Grid item xs={10} >
                    <Typography gutterBottom>{ sw.uri }</Typography>
                </Grid>

                <Grid item xs={2} >
                    <Typography variant="caption" gutterBottom>Name</Typography>
                </Grid>
                <Grid item xs={10} >
                    <Typography  component={'span'} gutterBottom>
                        { sw.name.map( (item, i) => <div  key={ 'swname'+i } >{item}<br /></div> ) }
                    </Typography>
                </Grid>

                <Grid item xs={2} >
                    <Typography variant="caption" gutterBottom>Version</Typography>
                </Grid>
                <Grid item xs={10} >
                    <Typography  component={'span'} gutterBottom>
                        { sw.version.map( (item, i) => <div  key={ 'swversion'+i } >{item}<br /></div> ) }
                    </Typography>
                </Grid>

                <Grid item xs={2} >
                    <Typography variant="caption" gutterBottom>Website</Typography>
                </Grid>
                <Grid item xs={10} >
                    <Typography  component={'span'} gutterBottom>
                        { sw.homepage.map( (item, i) => <div key={ 'swhomepage'+i } ><a href={item} target="_new"  rel="noopener noreferrer">{item}</a><br /></div> ) }
                    </Typography>
                </Grid>

            </Grid>

        </Grid>
    )
}

export default withStyles(styles) (PersonAgentProfile)
