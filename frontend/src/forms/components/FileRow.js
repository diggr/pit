/*
*
*  File display element for FilePicker Component
*
*/


import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { withStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import DescriptionIcon from '@material-ui/icons/Description'

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


class FileRow extends Component {

    renderButton () {
        const { currentFile, path, changeValue, name, classes } = this.props
        if (currentFile === path) 
            return (
                <Button 
                    color="primary"
                    size="small"
                    onClick={ () => { changeValue(path, false) } }
                >
                    <DescriptionIcon size="small" className={ classes.icon } />
                    { name }
                </Button>
            )
        else
            return (
                <Button 
                    size="small"
                    onClick={ () => { changeValue(path, false) } }
                >
                    <DescriptionIcon size="small" className={ classes.icon }  />
                    { name }
                </Button>                
            )
    }

    render ()  {
        const { classes } = this.props
        
        return (
            <div className={ classes.leftAlign } >
                { this.renderButton() }
            </div>
        )
    }
}

FileRow.propTypes = {
    currentFile: PropTypes.string,
    path: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    changeValue: PropTypes.func.isRequired
}

export default withStyles(styles) (FileRow)

