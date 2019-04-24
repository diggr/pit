import React, { Component } from 'react'

import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import IconButton from '@material-ui/core/IconButton'
import DeleteIcon from '@material-ui/icons/Delete'
import Avatar from '@material-ui/core/Avatar'
import { withStyles } from '@material-ui/core/styles'
import Typography from '@material-ui/core/Typography'
import FolderIcon from '@material-ui/icons/Folder'

import TransparentChip from '../../common/components/TransparentChip'

const styles = (theme) => ({
    directoryList: {
      padding: theme.spacing.unit * 4,
      marginTop: theme.spacing.unit * 8,
    },
    listItem: {
        padding: theme.spacing.unit *2,
        marginTop: theme.spacing.unit
    },
    directoryTitle: {
        textAlign: 'left',
        verticalAlign: 'middle' 
    },
    alignRight: {
        textAlign: 'right'
    },
    button: {
        margin: theme.spacing.unit,
    },
    tp: {
       
    },
    projectComment: {
        marginLeft: theme.spacing.unit * 5,
        marginTop: theme.spacing.unit * 0.5
    }
})

class DirectoryList extends Component {

    removeClick (directory) {
        this.props.removeDirectory(directory)
    } 

    render () {
        const { directories, classes } = this.props
        console.log(directories)
        return (
            <Grid container className={ classes.directoryList }>
                { directories.map( (item, i) => (
                    <Grid item xs={12} key={i} >
                        <Paper className={ classes.listItem }>
                            <Grid container
                                    className={ classes.directoryTitle } 
                            >
                                <Grid item xs={11} className={ classes.textAlign} >
                                    <div 
                                        className={ classes.tp } 
                                        onClick={ () => { this.props.history.push({ pathname: '/directory/', search: item.directory }) } }
                                    >
                                        <TransparentChip
                                            
                                            avatar={
                                                <Avatar>
                                                    <FolderIcon/>
                                                </Avatar>
                                                }                                                                                       

                                            className={ classes.button }
                                            
                                            label={ item.directory }  
                                        />
                                    </div>
                                    <div>
                                        <Typography variant="caption" className={ classes.projectComment }>
                                            { item.comment }
                                        </Typography>
                                    </div>
                                </Grid>
                                <Grid item xs={1} className={ classes.alignRight }>
                                    <IconButton aria-label="Delete"  onClick={ () => this.removeClick(item) }>
                                         <DeleteIcon size="small"  />
                                    </IconButton>
                                </Grid>
                            </Grid>
                        </Paper>
                    </Grid> 
                ) )}
            </Grid>
        )
    }
}


export default withStyles(styles) (DirectoryList)