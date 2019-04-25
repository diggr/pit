import React, { Component } from 'react'

import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import Paper from '@material-ui/core/Paper'
import { withStyles } from '@material-ui/core/styles'

const styles = theme => ({
    control: {
      padding: theme.spacing.unit * 4,
      marginTop: theme.spacing.unit * 8,
    },
})

class ConfigForm extends Component {

    componentDidMount() {
        this.props.fetchConfig()
    }

    handleChange = () => event => {
        this.props.updateProvitDir(event.target.value)
    }

    renderSaveButton = (enabled) => {
        if (this.props.changed) {
            return (
                <Button variant="contained">
                    Save changes
                </Button>
            )
        }
        else {
            return (
                <Button disabled variant="contained">
                    Save changes
                </Button>
            )            
        }
    }


    render () {
        const { classes } = this.props
        return (
            <div>
                <Grid container spacing={24}>
                    <Grid item xs={12}>
                        <Paper className={classes.control}>
                        <TextField
                            id="provit-home-directory"
                            label="Provit Home Directory"
                            style={{ margin: 8 }}
                            placeholder="Placeholder"
                            fullWidth
                            value={this.props.provitDir}
                            margin="normal"
                            InputLabelProps={{
                                shrink: true,
                            }}

                            onChange={this.handleChange()}
                        />
                        { this.renderSaveButton(this.props.changed) }

                        </Paper>
                    </Grid>
                </Grid>
            </div>
        )
    }
}


export default withStyles(styles) (ConfigForm)