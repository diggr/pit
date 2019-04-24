import React, { Component } from 'react'

import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core/styles'
import deepOrange from '@material-ui/core/colors/deepOrange'
import lime from '@material-ui/core/colors/lime'
import WarningIcon from '@material-ui/icons/Warning'
import Tooltip from '@material-ui/core/Tooltip'
import Chip from '@material-ui/core/Chip'
import Avatar from '@material-ui/core/Avatar'
import RefreshIcon from '@material-ui/icons/Refresh'

const styles = (theme) => ({
    fileTable: {
      padding: theme.spacing.unit * 4,
      marginTop: theme.spacing.unit * 3,
    },
    fileTablePaper: {
        padding: theme.spacing.unit*2
    },
    rowBackgroundNoProv: {
        backgroundColor: deepOrange[50]
    },
    rowBackgroundDiffLocation: {
        background: lime[50]
    },
    rowBackgroundProv: {
        backgroundColor: null
    },
    heading: {
        padding: theme.spacing.unit * 3
    },
    updateButton: {
        textAlign: 'right',
        paddingTop: theme.spacing.unit * 2
    }
})

class FileTable extends Component {

    linkToFile (item) {
        this.props.history.push({ pathname: "/file/", search: item.filepath })
    }

    renderTableRow (item, i) {
        const { classes } = this.props
        let cl = classes.rowBackgroundProv
        let warning = ""
        if (!item.prov) {
            cl = this.props.classes.rowBackgroundNoProv
        }
        else if (item.prov.last_location !== item.filepath ) {
            warning = "Changed file location"
            cl = classes.rowBackgroundDiffLocation
        }

        return (
            <TableRow 
                hover
                className={ cl } 
                key={ "filetable"+i } 
                onClick={ () => this.linkToFile(item) } 
            >
                <TableCell>{item.filename}</TableCell>
                <TableCell> { item.prov ? item.prov.last_activity : "No provenance information available!"} </TableCell>   
                <TableCell> { item.prov ? item.prov.timestamp : ""} </TableCell>   
                <TableCell>
                    { warning !== "" ? 
                       <Tooltip title={ warning }><WarningIcon /></Tooltip>
                      : ""
                    }
                </TableCell>
            </TableRow>         
        )
    }

    render () {
        const { classes, fileList, directory, updateFileList } = this.props

        let showUpdateFileLocations = false
        for (const item of fileList) {
            if (item.prov)
                if (item.prov.last_location !== item.filepath ) {
                    showUpdateFileLocations = true
                    break
                }
        }

        return (
            <Grid item xs={12} className={ classes.fileTable }>
                <Typography variant="h6" className={ classes.heading }>
                    {this.props.directory}
                </Typography>
                <Paper className={ classes.fileTablePaper }>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>File</TableCell>
                                <TableCell>Last Provenance Activity</TableCell>
                                <TableCell>Last Provenance Timestamp</TableCell>
                                <TableCell></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.props.fileList.map( (item, i) => this.renderTableRow(item, i) ) }                            
                        </TableBody>
                    </Table>

                    { showUpdateFileLocations ?
                        <Grid container>
                            <Grid item xs={12} className={ classes.updateButton }>
                                <Chip 
                                    size="small"
                                    onClick={ () => { updateFileList(directory) } }
                                    color="primary"
                                    avatar={
                                    <Avatar>
                                        <RefreshIcon />
                                    </Avatar>
                                    }
                                    label="Update provenance file locations"
                                />
                            </Grid>
                        </Grid>
                        : "" 
                    }
                </Paper>
            </Grid>
        )
    }
}

export default withStyles(styles) (FileTable)