import React, { Component } from 'react'
import path from 'path'
import { Control, Form, actions } from 'react-redux-form'
import { connect } from 'react-redux'
import { withStyles } from '@material-ui/core/styles'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import AddIcon from '@material-ui/icons/Add'
import Switch from '@material-ui/core/Switch'
import Typography from '@material-ui/core/Typography'

import FilePicker from '../components/FilePicker'
import AgentDropdown from '../components/AgentDropdown'

const styles = theme => ({
    formDialog: {
        padding: theme.spacing.unit*2
    },
    formGrid: {
        padding: theme.spacing.unit*2
    },
    formItem: {
        padding: theme.spacing.unit
    },
    inputField: {
        width: '100%'
    },
    agentColumn: {
        width: '66%'
    },
    buttonColumn: {
        width: '33%'
    }
})

class AddProvForm extends Component {

    state = {
        isTimestamp: true,
        timeValue: ""
    }

    componentDidMount () {
        const date = new Date()
        const timestamp = date.toISOString()
        this.setState({
            isTimestamp: true,
            timeValue: timestamp.substring(0, timestamp.length-2)            
        })
    }


    handleSubmit (prov) {
        const { handleSubmit, filepath, dispatch } = this.props
        console.log(prov)
        console.log(this.state.isTimestamp)
        handleSubmit(filepath, prov, this.state.isTimestamp)
        dispatch(actions.reset("addProvEvent"))
    }

    handleClose () {
        const { toggle, dispatch } = this.props
        dispatch(actions.reset("addProvEvent"))
        toggle()
    }

    toggleTimespan () {
        const date = new Date()
        const timestamp = date.toISOString()
        this.setState( { 
            isTimestamp: ! this.state.isTimestamp,
            timeValue: timestamp.substring(0, timestamp.length-2)
         })
    }

    render() {
        const { open, classes, dispatch, addProvEvent, filepath, agents } = this.props
        const initialAgent = ""
        const initialSource = ""

        return (
            <Dialog open={open} scroll="paper" onClose={ () => this.handleClose() } maxWidth="md" >
                <Form
                    model="addProvEvent"
                    onSubmit={(prov) => this.handleSubmit(prov)}
                >
                    <DialogContent>
                        <Grid container className={ classes.formGrid }>
                            <Grid item xs={12} className={ classes.formItem }>
                                <Control 
                                    className={ classes.inputField }
                                    component={TextField} 
                                    model="addProvEvent.activitySlug" 
                                    id="addProvEvent.activitySlug" 
                                    label="Activity slug" 
                                />
                            </Grid>

                            <Grid item xs={12} className={ classes.formItem }>
                                <Control  
                                    className={ classes.inputField }
                                    component={TextField} 
                                    model="addProvEvent.comment" 
                                    id="addProvEvent.comment" 
                                    label="Comment" 
                                    multiline 
                                    rowsMax="4" 
                                    variant="outlined" 
                                />
                            </Grid>

                            <Grid item xs={12} className={ classes.formItem }>
                                <Switch 
                                    value="isTimestamp" 
                                    checked={ !this.state.isTimestamp } 
                                    onClick={ () => this.toggleTimespan() } 
                                />
                                { this.state.isTimestamp ? "Timestamp" : "Timespan"}
                                
                            </Grid>

                            <Grid container >
                                <Grid item xs={5} className={ classes.formItem }>
                                    <Control  
                                        component={TextField} 
                                        type="datetime-local"
                                        model="addProvEvent.startedAt" 
                                        id="addProvEvent.startedAt" 
                                        label={this.state.isTimestamp ? "Timestamp" : "Started at" }
                                        defaultValue={ this.state.timeValue }
                                    />
                                </Grid>

                                { !this.state.isTimestamp ? 
                                <Grid item xs={5} className={ classes.formItem }>
                                    <Control  
                                        component={TextField} 
                                        type="datetime-local"
                                        model="addProvEvent.endedAt" 
                                        id="addProvEvent.endedAt" 
                                        label="Ended at"
                                        defaultValue={ this.state.timeValue }
                                    />
                                </Grid>
                                : "" }
                            </Grid>

                            <table>
                                <tbody>
                                <tr>
                                    <td >
                                        <Button 
                                            color="primary" 
                                            aria-label="Add" 
                                            size="small"
                                            onClick={() => dispatch(actions.push('addProvEvent.agents', initialAgent))}
                                        >
                                            <AddIcon />
                                            Agent
                                        </Button>       
                                    </td>
                                    <td className={ classes.inputField}>
                
                                        { addProvEvent.agents.map( (agent, i) => 
                                            <Grid container key={'provagent'+i}>
                                                <Grid item xs={12} className={ classes.formItem }>
                                                    <AgentDropdown
                                                        agents={ agents }
                                                        model={`addProvEvent.agents[${i}]`}
                                                        dispatch={ dispatch }
                                                    />                                                
                                                </Grid>                               
                                            </Grid>
                                        )}
                                    </td>                             
                                </tr>

                                <tr>
                                    <td>
                                        <Button 
                                            color="primary" 
                                            aria-label="Add" 
                                            size="small"
                                            onClick={() => dispatch(actions.push('addProvEvent.sources', initialSource))}
                                        >
                                            <AddIcon />
                                            Source
                                        </Button>       
                                    </td>
                                    <td className={ classes.agentColumn}>
                
                                        { addProvEvent.sources.map( (source, i) => 
                                            <Grid container key={'provsource'+i}>
                                                <Grid item xs={12} className={ classes.formItem }>
        
                                                    <FilePicker 
                                                        withFiles
                                                        helptext="Select file"
                                                        model={ `addProvEvent.sources[${i}]` }  
                                                        directory={ path.dirname(filepath) } 
                                                        dispatch={ dispatch } 
                                                    /> 
                                                </Grid>                               
                                            </Grid>
                                        )}
                                    </td>                             
                                </tr>
    
                                <tr>
                                    <td>
                                        <Button 
                                            color="primary" 
                                            aria-label="Add" 
                                            size="small"
                                            onClick={() => dispatch(actions.push('addProvEvent.primarySources', initialSource))}
                                        >
                                            <AddIcon />
                                            Primary Source
                                        </Button>       
                                    </td>
                                    <td className={ classes.agentColumn}>
                
                                        { addProvEvent.primarySources.map( (source, i) => 
                                            <Grid container key={'provsource'+i}>
                                                <Grid item xs={12} className={ classes.formItem }>
                                                    <AgentDropdown
                                                        agents={ agents }
                                                        model={ `addProvEvent.primarySources[${i}]` }
                                                        dispatch={ dispatch }
                                                    />
                                                </Grid>                               
                                            </Grid>
                                        )}
                                    </td>                             
                                </tr>
                                </tbody>
                            </table>                                

                        </Grid>

                    </DialogContent>
                    <DialogActions  className={ classes.formDialog }>
                        <Button type="submit" color="primary" variant="contained" >
                            Add Provenance Information
                        </Button>
                    </DialogActions>
                    </Form>

            </Dialog>
        )
    }
}

const ProvForm = withStyles(styles) ( AddProvForm)

export default connect( ({addProvEvent})  =>  ({addProvEvent}) ) (ProvForm)