import React, { Component } from 'react'
import PropTypes from 'prop-types'

import LaptopIcon from '@material-ui/icons/Laptop'
import FaceIcon from '@material-ui/icons/Face'
import BusinessIcon from '@material-ui/icons/Business'
import Avatar from '@material-ui/core/Avatar'
import Chip from '@material-ui/core/Chip'

class AgentIcon extends Component {
    render () {
        const { type, slug } = this.props
        const handleClick = () => {}
        switch (type) {
            case 'Person':
                return (
                    <div>
                    <Chip
                        onClick={ () => { handleClick() }}
                        avatar={
                        <Avatar>
                            <FaceIcon />
                        </Avatar>
                        }
                        label={ slug }
                    />
                    </div>
                )  
            case 'Organization':
                return (
                    <div>
                    <Chip
                        onClick={ () => { handleClick() }}                    
                        avatar={
                        <Avatar>
                            <BusinessIcon />
                        </Avatar>
                        }
                        label={ slug }
                    />
                    </div>
                )    
            case 'SoftwareAgent':
                return (
                    <div>
                    <Chip
                        onClick={ () => { handleClick() }}                    
                        avatar={
                        <Avatar>
                            <LaptopIcon />
                        </Avatar>
                        }
                        label={ slug }
                    />
                    </div>
                )                                   
            default:
                return ""
        }
    }
}

AgentIcon.propTypes = {
    type: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired
}

export default AgentIcon