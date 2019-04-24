import React, { Component } from 'react'
import { Control, Form, actions } from 'react-redux-form'
import { connect } from 'react-redux'

import { withStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'
import TextField from '@material-ui/core/TextField'
import Dialog from '@material-ui/core/Dialog'
import Fab from '@material-ui/core/Fab'
import AddIcon from '@material-ui/icons/Add'
import Button from '@material-ui/core/Button'
import DialogActions from '@material-ui/core/DialogActions'

import FilePicker from '../components/FilePicker'

const styles = (theme) => ({
    formContainer: {
        padding: theme.spacing.unit*2
    },
    formItem: {
        padding: theme.spacing.unit*2
    },
    inputField: {
        width: '100%'
    }
})

class AddProjectDirectoryForm extends Component {

    constructor (props) {
        super(props)
        this.state = {
            open: false
        }
    }

    handleSubmit (directory) {
        const  { handleSubmit } = this.props
        console.log (directory)
        handleSubmit(directory)
        this.closeDialog()
    }

    toggleDialog () {
        this.setState({
            open: !this.state.open
        })
    }

    closeDialog () {
        const { dispatch } = this.props
        dispatch(actions.reset("addProjectDirectory"))
        this.toggleDialog()
    }

    render () {
        const { classes, dispatch } = this.props

        return (
            <div>
                <Dialog open={ this.state.open } onClose={ () => this.closeDialog() }>
                    <Form
                        model="addProjectDirectory"
                        onSubmit={(dir) => this.handleSubmit(dir)}
                    >
                        <Grid container className={ classes.formContainer }>
                            <Grid item xs={12} className={ classes.formItem }>

                                <FilePicker 
                                    id="addProjectDirectory.directory"
                                    model="addProjectDirectory.directory"  
                                    helptext="Select directory"
                                    withFiles={ false }
                                    directory={ '' } 
                                    dispatch={ dispatch } 
                                /> 

                            </Grid>

                            <Grid item xs={12} className={ classes.formItem }>
                                <Control  
                                    className={ classes.inputField }
                                    component={TextField} 
                                    model="addProjectDirectory.comment" 
                                    id="addProjectDirectory.comment" 
                                    label="Comment" 
                                    multiline 
                                    rowsMax="4" 
                                    variant="outlined" 
                                />
                            </Grid>
                        </Grid>

                        <DialogActions>
                            <Button type="submit" color="primary" variant="contained" >
                                Add
                            </Button>
                        </DialogActions>   
                    </Form>                   
                </Dialog>
                  
                <Fab 
                    color="primary" 
                    aria-label="Add" 
                    className={classes.fab} 
                    onClick={ () => this.toggleDialog() }
                >
                    <AddIcon />
                </Fab>           
            </div>
        )
    }
}

const projectForm = withStyles(styles) (AddProjectDirectoryForm)

export default connect( ({addProjectDirectory})  =>  ({addProjectDirectory}) ) (projectForm)

