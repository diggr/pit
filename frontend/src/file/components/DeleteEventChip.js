import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { withStyles } from '@material-ui/core/styles'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import Button from '@material-ui/core/Button'
import Chip from '@material-ui/core/Chip'
import Avatar from '@material-ui/core/Avatar'
import RemoveIcon from '@material-ui/icons/Remove'


const styles = (theme) => ({
    removeProv: {
        marginLeft: theme.spacing.unit*2
    }
})

class DeleteEventChip extends Component {
    state = {
        open: false
    }

    handleClickOpen () {
        this.setState({ open: true })
    }

    handleClose () {
        this.setState({ open: false })
    }

    handleDelete () {
        const { removeProv, currentFile } = this.props
        removeProv(currentFile)
        this.handleClose()
    }

    render () {

        const { classes } = this.props

        return (
            <span>
                <Chip 
                    size="small"
                    className={ classes.removeProv }
                    onClick={ () => this.handleClickOpen() }
                    color="secondary"
                    avatar={
                    <Avatar>
                        <RemoveIcon />
                    </Avatar>
                    }
                    label="Delete Event"
                />
                <Dialog
                    open={ this.state.open }
                    onClose={ () => this.handleClose() }
                >
                    <DialogContent>
                        Do you really want to delete the last provenance event?
                    </DialogContent>
                    <DialogActions>
                        <Button 
                            color="primary" 
                            variant="contained"
                            onClick={ () => this.handleDelete() }
                        >
                            Delete
                        </Button>
                        <Button 
                            color="secondary" 
                            variant="contained" 
                            onClick={ () => this.handleClose() }
                        >
                            Cancel
                        </Button>
                    </DialogActions>
                </Dialog>                
            </span>
        )
    }
}

DeleteEventChip.propTypes = {
    removeProv: PropTypes.func.isRequired,
    currentFile: PropTypes.string.isRequired
}

export default withStyles(styles) (DeleteEventChip)