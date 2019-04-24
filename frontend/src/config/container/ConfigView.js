import { connect } from 'react-redux'
import * as api from '../api'
import * as actions from '../actions'
import ConfigForm from '../components/ConfigForm'

const mapStateToProps = (state) => ({
    provitDir: state.config.provitDir,
    changed: state.config.changed
})

const mapDispatchToProps = {
    fetchConfig: api.fetchConfig,
    updateProvitDir: actions.updateProvitDir
}

const ConfigView = connect(mapStateToProps, mapDispatchToProps) (ConfigForm)

export default ConfigView