import React, { Component } from 'react'
import { withStyles } from '@material-ui/core'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'

import AgentIcon from '../../common/components/AgentIcon'
import AgentDialog from './AgentDialog'

const styles = theme => ({
    alignLeft: {
        textAlign: 'left',
        padding: theme.spacing.unit *2,
    },
    agentIcon: {
        paddingRight: theme.spacing.unit
    }
})

class EventDetails extends Component {

    constructor (props) {
        super(props)
        this.eventData = {}
    }

    getEventData (root) {
        const { currentProvEvent } = this.props
        if (root.uri === currentProvEvent)
            this.eventData = root
        else {
            if (root.sources)
                for (const source of root.sources)
                    this.getEventData(source)
        }
    }

    handleAgentIconClick = (agentSlug) => {
        this.props.setCurrentAgent(agentSlug)
    }

    renderAgent (slug) {
        const { agents, classes } = this.props

        if (slug in agents) {
            return (
                <div className={ classes.agentIcon } key={ 'agenticon'+slug } onClick={ () => { this.handleAgentIconClick(slug) } } > 
                    <AgentIcon 
                        type={agents[slug].type}
                        slug={slug}
                    />
                </div>
            )
        }
        else {
            return (
                <div key={"displayagent-"+slug}>{slug}</div>
            )
        }
    }

    render () {

        const { classes, prov, currentProvEvent, currentAgent, agents } = this.props
        const agentData = agents[currentAgent]
        let agentSlugs = []

        if (currentProvEvent) {
            this.getEventData(prov)      
            agentSlugs = this.eventData.agent.map( (item) => item.split('/')[item.split('/').length -1] )
            
        }
        else {
            this.eventData = {}
        }

        let timespan =  this.eventData.ended_at
        if (this.eventData.started_at) 
            timespan = this.eventData.started_at + " - " + this.eventData.ended_at

        return (
            <div>
                <Paper className={ classes.alignLeft }>

                    <Typography variant="caption" gutterBottom>
                        <b>Event URI</b>
                    </Typography>                    
                    <Typography  variant="caption" gutterBottom>
                        {this.eventData.uri}
                    </Typography>

                    <Typography variant="caption" gutterBottom>
                        <b>Timestamp</b>
                    </Typography>  
                    <Typography  variant="caption" gutterBottom>
                        { timespan }
                    </Typography>                    

                    <Typography variant="caption" gutterBottom>
                        <b>Description</b>
                    </Typography>  
                    <Typography  variant="caption" gutterBottom>
                        {this.eventData.activity_desc}
                    </Typography>    

                    <Typography variant="caption" gutterBottom className="break">
                        <b>File location</b>
                    </Typography>  
                    <Typography  variant="caption" gutterBottom>
                        {this.eventData.location}
                    </Typography>    

                    <Typography variant="caption" gutterBottom>
                        <b>Agents</b>
                    </Typography>  
                    <div>
                        <div className="agentIconList"> 
                        {agentSlugs.map( (item) => this.renderAgent(item) ) }
                        </div>
                    </div>      

                    <div className="break" ></div>
                    { currentAgent ? 
                        <AgentDialog 
                            open={this.props.showAgentDialog}
                            hideAgentDialog={this.props.hideAgentDialog}
                            data={agentData}
                        /> : ""
                    }
                </Paper>
            </div>
        )
    }
}

export default withStyles(styles) (EventDetails)