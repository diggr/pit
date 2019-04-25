import React, { Component } from 'react'
import { withRouter } from 'react-router'

import { withStyles } from '@material-ui/core/styles'
import Typography from '@material-ui/core/Typography'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';

const styles = (theme) => ({
    title: {
        marginRight: theme.spacing.unit * 2,
    }
})

class Menu extends Component {


    render () {
        return (
            <AppBar>
                <Toolbar>
                    <Typography color="inherit" component="h3" variant="display1" className={ this.props.classes.title }>
                        provit
                    </Typography>

                    <Button color="inherit" onClick={ () => { this.props.history.push("/") } }>
                    Files
                    </Button>
                    <Button color="inherit" onClick={ () => { this.props.history.push("/agents/") } }>
                    Agents
                    </Button>
                </Toolbar>
            </AppBar>        
        )
    }
}

const menu = withStyles(styles) (Menu)

export default withRouter(menu)