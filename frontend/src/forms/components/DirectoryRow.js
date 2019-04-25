/*
*
*  Directory display element for FilePicker Component
*
*/

import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { withStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import FolderIcon from '@material-ui/icons/Folder'
import MoreHorizIcon from '@material-ui/icons/MoreHoriz'

const styles = theme => ({
    leftAlign: {
        textAlign: 'left',
        width: '100%'
    },
    fullWidth: {
        width: '100%'
    },
    icon: {
        marginRight: theme.spacing.unit
    }
})


class DirectoryRow extends Component {

    renderButton () {
        const { currentFile, path, changeValue, name, classes, selectable } = this.props
        if (currentFile === path) 
            return (
                <Button 
                    color="primary"
                    size="small"
                    onClick={ () => { if (selectable) changeValue(path, false) } }
                >
                    <FolderIcon size="small" className={ classes.icon } />
                    { name }
                </Button>
            )
        else
            return (
                <Button 
                    size="small"
                    onClick={ () => {  if (selectable) changeValue(path, false) } }
                >
                    <FolderIcon size="small" className={ classes.icon }  />
                    { name }
                </Button>                
            )
    }

    render ()  {
        const { classes, path, fetchDir } = this.props
        
        return (
            <div className={ classes.leftAlign } >

                { this.renderButton() }

                <Button 
                    size="small"
                    onClick={  () => { fetchDir(path) }  }
                >
                    <MoreHorizIcon size="small" />
                </Button>
            </div>
        )
    }
}

DirectoryRow.propTypes = {
    name: PropTypes.string.isRequired,
    path: PropTypes.string.isRequired,
    currentFile: PropTypes.string.isRequired,
    fetchDir: PropTypes.func.isRequired,
}

export default withStyles(styles) (DirectoryRow)

