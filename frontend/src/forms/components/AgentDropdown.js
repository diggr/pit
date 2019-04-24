import React, { Component } from 'react'
import { actions } from 'react-redux-form'
import PropTypes from 'prop-types'

import { withStyles } from '@material-ui/core/styles'
import TextField from '@material-ui/core/TextField'
import MenuItem from '@material-ui/core/MenuItem'
import LaptopIcon from '@material-ui/icons/Laptop'
import FaceIcon from '@material-ui/icons/Face'
import BusinessIcon from '@material-ui/icons/Business'
import Avatar from '@material-ui/core/Avatar'

import TransparentChip from '../../common/components/TransparentChip'

const styles = (theme) => ({
    textField: {
        width: '100%'
      },
    menuItem: {
        width: '100%',
        padding: theme.spacing.unit
    }
})



class AgentDropdown extends Component {

    constructor (props) {
        super(props)

        this.state = {
            modelValue: ""
        }

    }

    handleChange (event) {
        const { model, dispatch } = this.props

        const value = event.target.value
        this.setState({
            modelValue: value
        })
        dispatch(actions.change(model, value))
    }

    getAgentsByType (agentType) {
        const { agents } = this.props
        const slugs = []
        for (const slug of Object.keys(agents)) {
            if (agents[slug].type === agentType)
                slugs.push(slug)
        }
        return slugs
    }

    render () {
        const { classes, agents } = this.props

        return (
            <TextField
                select
                margin="normal"
                value={this.state.modelValue}
                className={classes.textField}
                SelectProps={{
                    MenuProps: { className: classes.menuItem }
                }}
                onChange={ (e) => this.handleChange(e) }
            >
                { agents.persons.map( (agent,i) => (
                    <MenuItem key={ agent.slug } value={ agent.slug } className={ classes.menuItem } >
                        <TransparentChip
                            avatar={
                            <Avatar>
                                <FaceIcon />
                            </Avatar>
                            }
                            label={ agent.slug }
                        />
                    </MenuItem>
                ) ) }
                { agents.software.map( (sw,i) => (
                    <MenuItem key={ sw.slug } value={ sw.slug } className={ classes.menuItem } >
                        <TransparentChip
                            avatar={
                            <Avatar>
                                <LaptopIcon />
                            </Avatar>
                            }
                            label={ sw.slug }
                        />
                    </MenuItem>
                ) ) }
                { agents.organizations.map( (sw,i) => (
                    <MenuItem key={ sw.slug } value={ sw.slug } className={ classes.menuItem } >
                        <TransparentChip
                            avatar={
                            <Avatar>
                                <BusinessIcon />
                            </Avatar>
                            }
                            label={ sw.slug }
                        />
                    </MenuItem>
                ) ) }                
                
            </TextField>
        )
    }
}
AgentDropdown.propTypes = {
    agents: PropTypes.object.isRequired,
    model: PropTypes.string.isRequired,
    dispatch: PropTypes.func.isRequired
}

export default withStyles(styles) (AgentDropdown)