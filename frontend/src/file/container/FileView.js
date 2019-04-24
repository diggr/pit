import React, { Component } from 'react'
import { connect } from 'react-redux'
import * as actions from '../actions'
import * as api from '../api'
import * as agentApi from '../../agents/api'

import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Chip from '@material-ui/core/Chip'
import { withStyles } from '@material-ui/core/styles'
import Avatar from '@material-ui/core/Avatar'
import AddIcon from '@material-ui/icons/Add'

import EventNetwork from '../components/EventNetwork'
import EventTimeline from '../components/EventTimeline'
import EventDetails from '../components/EventDetails'
import AddProvForm from '../../forms/container/AddProvForm'
import DeleteEventChip from '../components/DeleteEventChip'

const mapStateToProps = (state) => ({
    hasProv: state.file.hasProv,
    prov: state.file.prov,
    currentFile: state.file.currentFile,
    agents: state.file.agents,
    allAgents: state.agents,
    currentProvEvent: state.file.currentProvEvent,
    updateNetwork: state.file.updateNetwork,
    rebuildNetwork: state.file.rebuildNetwork,
    currentAgent: state.file.currentAgent,
    showAgentDialog: state.file.showAgentDialog,
    showAddProvForm: state.file.showAddProvForm
})

const mapDispatchToProps = {
    changeCurrentFile: actions.changeCurrentFile,
    fetchProv: api.fetchProv,
    addProv: api.addProv,
    removeProv: api.removeProv,
    changeProvEvent: actions.changeProvEvent,
    networkUpdated: actions.networkUpdated,
    setCurrentAgent: actions.setCurrentAgent,
    hideAgentDialog: actions.hideAgentDialog,
    toggleAddProvForm: actions.toggleAddProvForm,
    fetchAgents: agentApi.fetchAgents,
    resetFileState: actions.resetFileState
}

const styles = theme => ({
    fileViewContainer: {
        marginTop: 30
    },
    breadcrumbs: {
        marginBottom: theme.spacing.unit*2,
        textAlign: 'left'
    },
    directory: {
        paddingRight: theme.spacing.unit*2
    },
    filename: {
        lineHeight:2,
        vertialAlign: 'middle'
    },
    addProv: {
        marginLeft: 20,
    },
    provButtons: {
        marginBottom: theme.spacing.unit,
        textAlign: 'right'
    },    
})

const splitFilepath = (filepath) => {
    const split = filepath.split('/')
    const slug = split[split.length-1]
    const dir = filepath.replace(slug, '')
    return [dir, slug]
}

class FileView extends Component {

    componentDidMount() {
        const filepath = this.props.location.search.substr(1)
        if (filepath !== this.props.currentFile) {
            this.props.fetchProv(filepath)
            this.props.changeCurrentFile(filepath)
        }
        console.log(this.props)

        // if no allAgents are not loaded fetch them from the api
        if (this.props.allAgents.persons.length === 0)
            this.props.fetchAgents()
    }
    
    componentDidUpdate() {
        const filepath = this.props.location.search.substr(1)
        if (filepath !== this.props.currentFile) {
            this.props.changeCurrentFile(filepath)
        }
    }

    componentWillUnmount() {
        this.props.resetFileState()
    }

    render() {
        const { classes, currentFile, showAddProvForm, toggleAddProvForm, allAgents, addProv } = this.props

        let filepath
        if (currentFile) {        
            filepath = splitFilepath(currentFile)      
        }

        return (
            <div className={ classes.fileViewContainer }  >

                <AddProvForm 
                    open={ showAddProvForm} 
                    handleSubmit={ addProv }
                    toggle={ toggleAddProvForm } 
                    agents={ allAgents }
                    filepath={ currentFile }
                />

                <Grid container>
                    <Grid container className={ classes.breadcrumbs }>
                        <Grid item xs={8}>
                            { currentFile ?
                            <Grid container>
                                <Grid item className={ classes.directory }>
                                    <Chip 
                                        onClick={ () => { this.props.history.push({
                                            pathname: "/directory/", 
                                            search: filepath[0] 
                                        }) } }
                                        label={ filepath[0] }  />
                                </Grid>
                                <Grid item >
                                    <Typography variant="subtitle1" gutterBottom className={ classes.filename }>
                                        { filepath[1] }
                                    </Typography>
                                </Grid>
                            </Grid>
                            : ""  }
                        </Grid>

                        <Grid item xs={4} className={ classes.provButtons }>                  
                            <Chip 
                                size="small"
                                className={ classes.addProv }
                                onClick={ () => { this.props.toggleAddProvForm() } }
                                color="primary"
                                avatar={
                                <Avatar>
                                    <AddIcon />
                                </Avatar>
                                }
                                label="Add Event"
                            />
                            <DeleteEventChip 
                                currentFile={ currentFile } 
                                removeProv={ this.props.removeProv }
                            />

                        </Grid>
                    </Grid>

                    { true ?
                    <Grid container>
                        <Grid item xs={12}>
                                <EventTimeline 
                                    prov={this.props.prov ? this.props.prov : {} } 
                                    changeProvEvent={this.props.changeProvEvent} 
                                    currentProvEvent={this.props.currentProvEvent} 
                                    rebuildNetwork={this.props.rebuildNetwork}
                                />
                        </Grid>
                        <Grid item xs={8}>
                            
                                <EventNetwork 
                                    prov={this.props.prov ? this.props.prov : {} } 
                                    changeProvEvent={this.props.changeProvEvent} 
                                    currentProvEvent={this.props.currentProvEvent} 
                                    updateNetwork={this.props.updateNetwork}
                                    rebuildNetwork={this.props.rebuildNetwork}
                                    networkUpdated={this.props.networkUpdated}
                                />
                        </Grid>
                        <Grid item xs={4}>
                            { this.props.currentProvEvent ? 
                                <EventDetails
                                    prov={this.props.prov ? this.props.prov : {} } 
                                    agents={this.props.agents}
                                    currentProvEvent={this.props.currentProvEvent}
                                    currentAgent={this.props.currentAgent}
                                    rebuildNetwork={this.props.rebuildNetwork}
                                    showAgentDialog={this.props.showAgentDialog}
                                    hideAgentDialog={this.props.hideAgentDialog}
                                    setCurrentAgent={this.props.setCurrentAgent}
                                />
                            : "" }
                        </Grid>
                    </Grid>
                    : "" }
                </Grid>
            </div>
        )
    }
}

const fileView = withStyles(styles) (FileView)

export default connect(mapStateToProps, mapDispatchToProps)(fileView)