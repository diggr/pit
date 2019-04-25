/*

FilePicker Component

Opens Dialog representing the contents of the workstations file system
Move up and down the file system
Select a file, which will be stored in the components value state and updates the model

TODO:
* show only directories
* allow to select directories

Props:
- directory: starting directory
- model: name of forms model

*/

import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { actions } from 'react-redux-form'
import path from 'path'

import { withStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog'
import DialogContent from '@material-ui/core/DialogContent'
import DialogActions from '@material-ui/core/DialogActions'
import DialogTitle from '@material-ui/core/DialogTitle'
import IconButton from '@material-ui/core/IconButton'
import FolderIcon from '@material-ui/icons/Folder'
import Typography from '@material-ui/core/Typography'
import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward'

import DirectoryRow from './DirectoryRow'
import FileRow from './FileRow'

const styles = theme => ({
    filebrowserDialog: {
        padding: theme.spacing.unit*2,
    },
    dialogPaper: {
        minHeight: '70vh',
        maxHeight: '70vh',
    },
    helptext: {
        color: '#999',
        text: '0.8em'
    }
})


class FilePicker extends Component {

    constructor (props) {
        super(props)

        let { withFiles } = props
        if (withFiles)
            withFiles = true
        else
            withFiles = false

        this.state = {
            showDialog: false,
            currentDir: "",
            withFiles: withFiles,
            files: [],
            dirs: [],
            value: ""
        }

        this.changeValue = this.changeValue.bind(this)
        this.fetchDir = this.fetchDir.bind(this)
    }

    componentDidMount () {
        const { directory } = this.props
        this.setState({
            currentDir: directory
        })
        this.fetchDir(directory)
    }

    fetchDir (dir) {

        fetch('http://localhost:5555/filebrowser',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },            
            mode: 'cors',
            body: JSON.stringify({ directory: dir, withFiles: this.state.withFiles, withHidden: false })
            })
            .then(res => res.json())
            .then(json => {
                console.log(json)
                this.setState({
                    ...this.state,
                    dirs: json.dirs,
                    files: json.files,
                    currentDir: dir
                })
                return json.prov
            })
            .catch(error => console.log(error))        
    }

    openDialog () {
            this.setState({
                showDialog: true
            })
    }

    closeDialog () {
        this.setState({
            showDialog: false
        })
    }

    changeValue (value, close) {
        const { model, dispatch } = this.props
        const showDialog = !close

        this.setState({
            value,
            showDialog
        })
        dispatch(actions.change(model, value))
    }

    render () {

        const { directory, classes, helptext } = this.props
        const { showDialog, dirs, files, currentDir, value } = this.state
        const pathSplit = currentDir.split(path.sep)
        pathSplit.splice(-1, 1)
        const parentDir = path.resolve( ...pathSplit)
        const currentValueSplit = this.state.value.split(path.sep)
        const currentValue = currentValueSplit.pop()

        const selectableDirectories = !this.state.withFiles

        return (
            <div>
                
                <Dialog
                    fullWidth={ true }
                    maxWidth="sm"
                    open={ showDialog }
                    scroll="paper"
                    className={ classes.filebrowserDialog }
                    classes={ { paper: classes.dialogPaper } }
                    onClose={ () => this.changeValue("", true) }
                >
                    <DialogTitle>
                        <div>
                        <Typography variant="subheading"> { currentDir }</Typography>
                        </div>
                    </DialogTitle>
                    <DialogContent>
                        <Button 
                            size="small"
                            onClick={ () => this.fetchDir(parentDir) }
                        >
                            <ArrowUpwardIcon size="small" />
                        </Button>

                        { dirs.map( (dir, i) => 
                            <DirectoryRow 
                                key={'directory'+i} 
                                name={dir.dirname} 
                                path={dir.dirpath}
                                selectable={ selectableDirectories }
                                changeValue={ this.changeValue }
                                fetchDir={ this.fetchDir }
                                currentFile={ value }
                            /> 
                        ) }
                        { files.map( (file, i) => 
                            <FileRow 
                                key={'file'+i} 
                                name={file.filename} 
                                path={file.filepath}
                                changeValue={ this.changeValue }
                                currentFile={ value }
                            /> 
                        ) }
                    </DialogContent>
                    <DialogActions>
                        <Button 
                            color="primary" 
                            variant="contained" 
                            onClick={ () => this.closeDialog() }
                        >
                            Select
                        </Button>
                        <Button 
                            color="secondary" 
                            variant="contained" 
                            onClick={ () => this.changeValue("", true) }
                        >
                            Close
                        </Button>
                    </DialogActions>                    
                </Dialog>

                <IconButton
                    variant="contained"
                    onClick={ () => this.openDialog(directory) }
                >
                    <FolderIcon size="small" />
                </IconButton>            
                    <Button  onClick={ () => this.openDialog(directory) } >{ currentValue || helptext  }</Button> 
  
            </div>
        )
    }
}

FilePicker.propTypes = {
    directory: PropTypes.string,
    model: PropTypes.string,
    dispatch: PropTypes.func
}

export default withStyles(styles) (FilePicker)

