import React, { Component } from 'react'
import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'

import AgentIcon from '../../common/components/AgentIcon'
import PersonAgentProfile from '../../common/components/PersonAgentProfile'
import OrgAgentProfile from '../../common/components/OrgAgentProfile'
import SoftwareAgentProfile from '../../common/components/SoftwareAgentProfile'

class AgentDialog extends Component {

    handleClose () {
        this.props.hideAgentDialog()
    }

    renderPersonAgentDialog () {
        const { data } = this.props
        return (
            <div>
                <PersonAgentProfile person={ data } />
            </div>                  
        )
    }

    renderSoftwareAgentDialog () {
        const { data } = this.props
        return (
            <div>
                <SoftwareAgentProfile sw={ data } />
            </div>                  
        )
    }    

    renderOrgAgentDialog () {
        const { data } = this.props
        return (
            <div>
                <OrgAgentProfile org={ data } />
            </div>
        )
    }    

    renderAgentDialog () {
        const { data } =  this.props
        switch (data.type) {
            case 'Person':
                return this.renderPersonAgentDialog()
            case 'Organization':
                return this.renderOrgAgentDialog()
            case 'SoftwareAgent':
                return this.renderSoftwareAgentDialog()                                
            default:
                return ""
        }
    }

    render () {
        const { open, data } = this.props

        return (
            <div>
                <Dialog
                    onClose={ () => this.handleClose() } 
                    open={open}
                >
                    <DialogTitle>
                        <AgentIcon 
                            type={data.type}
                            slug={data.slug}
                        />
                    </DialogTitle>
                    <DialogContent>
                        <DialogContentText component="span">
                            { this.renderAgentDialog() }
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={ () => { this.handleClose() } } color="primary" autoFocus>
                            Close
                        </Button>
                    </DialogActions>                    
                </Dialog>
            </div>
        )
    }
}

export default AgentDialog