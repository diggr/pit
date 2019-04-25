import React, { Component } from 'react'

import Grid from '@material-ui/core/Grid'
import { withStyles } from '@material-ui/core/styles'
import ExpansionPanel from '@material-ui/core/ExpansionPanel'
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails'
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'
import Typography from '@material-ui/core/Typography'
import BusinessIcon from '@material-ui/icons/Business'
import Avatar from '@material-ui/core/Avatar'
import Chip from '@material-ui/core/Chip';

const styles = theme => ({
    root: {
        flexGrow: 1,
      },
    content: {
      padding: theme.spacing.unit * 4,
      marginTop: theme.spacing.unit * 4,
    },
    paperLayout: {
        padding: theme.spacing.unit * 2
    },
    detailsBox: {
        textAlign: 'left',
    },
    detailsBoxHeader: {
        textAlign: 'left',
        marginRight: theme.spacing.unit*2
    },
    agentHeader: {
        padding:theme.spacing.unit
    },
    nameHeader: {
        lineHeight: 2.3
    }
})

class SoftwareAgentList extends Component {

    renderSoftware(org, i) {
        const { classes } = this.props
        return (
            <div key={ "org"+i }>
                <ExpansionPanel>
                    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <Grid container>
                        <Grid item className={ classes.detailsBoxHeader }>
                        <Chip
                            avatar={
                            <Avatar>
                                <BusinessIcon />
                            </Avatar>
                            }
                            label={ org.slug }
                        />
                        </Grid>
                        <Grid item className={ classes.detailsBoxHeader }>
                        <Typography className={ classes.nameHeader } >{ org.name[0] }</Typography>
                        </Grid>
                    </Grid>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <Grid container>
                            <Grid item xs={1} className={ classes.detailsBox }>
                                <Typography variant="caption" gutterBottom>URI</Typography>
                            </Grid>
                            <Grid item xs={11} className={ classes.detailsBox }>
                                <Typography gutterBottom>{ org.uri }</Typography>
                            </Grid>

                            <Grid item xs={1} className={ classes.detailsBox }>
                                <Typography variant="caption" gutterBottom>Name</Typography>
                            </Grid>
                            <Grid item xs={11} className={ classes.detailsBox }>
                                <Typography component={'span'} gutterBottom>{ org.name.map( (item, i) => <div key={'orgname'+i }>{item}<br /></div> ) }</Typography>
                            </Grid>

                            <Grid item xs={1} className={ classes.detailsBox }>
                                <Typography variant="caption" gutterBottom>Website</Typography>
                            </Grid>
                            <Grid item xs={11} className={ classes.detailsBox }>
                                <Typography gutterBottom><a href={ org.homepage } target="_blank"  rel="noopener noreferrer">{ org.homepage }</a></Typography>
                            </Grid>

                        </Grid>
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </div>
        )
    }

    render () {
        const { organizations, classes } = this.props

        return (
            <Grid container className={ classes.root }>
                <Grid item xs={12} className={ classes.content }>
                    Organizations
                    <div className={ classes.paperLayout }>
                        { organizations.map( (item, i) => this.renderSoftware(item, i) ) }
                    </div>
                </Grid>
            </Grid>
        )
    }
}

export default withStyles(styles) (SoftwareAgentList)