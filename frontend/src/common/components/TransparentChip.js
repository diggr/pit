import React from 'react'
import PropTypes from 'prop-types'

import { withStyles } from '@material-ui/core/styles'
import Chip from '@material-ui/core/Chip'

const styles = theme => ({
    transparentChip: {
        backgroundColor: 'rgba(0,0,0,0.0);',
        cursor: 'pointer'
    }
})

const TransparentChip = (props) => (
    <Chip   
        label={ props.label }
        avatar={ props.avatar }
        className={ props.classes.transparentChip }
    />
)
TransparentChip.propTypes = {
    label: PropTypes.string.isRequired,
    avatar: PropTypes.object.isRequired,
}

export default withStyles(styles) (TransparentChip)