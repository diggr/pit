import React, { Component } from 'react'

import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid'
import Fab from '@material-ui/core/Fab'
import AddIcon from '@material-ui/icons/Add'
import { withStyles } from '@material-ui/core/styles'

const styles = theme => ({
    control: {
      padding: theme.spacing.unit * 4,
      marginTop: theme.spacing.unit * 8,
    },
})

class AddDirectoryForm extends Component {

    constructor (props) {
        super(props);
        this.state = { textField: "/" };
    }

    handleTextFieldUpdate (evt) {
        this.setState({ textField: evt.target.value })  
    }

    render () {
        const { classes, addDirectory } = this.props

        return (
            <Grid container spacing={24}>
                <Grid item xs={12}>
                    <TextField
                        id="add-directory-textfield"
                        label="Add Directory"
                        style={{ width: "80%" }}
                        placeholder=""
                        margin="normal"
                        value={ this.state.textField }
                        onChange={ (evt) => this.handleTextFieldUpdate(evt) }
                    />
                    <Fab 
                        color="primary" 
                        aria-label="Add" 
                        className={classes.fab} 
                        onClick={ () => addDirectory(this.state.textField) }
                    >
                        <AddIcon />
                    </Fab>
                </Grid>
            </Grid>
        )
    }
}

export default withStyles(styles) (AddDirectoryForm)