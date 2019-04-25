import React, { Component } from 'react'
import { connect } from 'react-redux'
import * as api from '../api'

import DirectoryList from '../components/DirectoryList'
import AddDirectoryProjectForm from '../../forms/container/AddProjectDirectoryForm'

const mapStateToProps = (state) => ({
    directories: state.home.directories,
    loading: state.home.loading,
    error: state.home.error
})

const mapDispatchToProps = {
    fetchDirectories: api.fetchDirectories,
    removeDirectory: api.removeDirectory,
    addDirectory: api.addDirectory
}

class HomeView extends Component {

    componentDidMount () {
        this.props.fetchDirectories()
    }

    render () {
        return (
            <div>
                <DirectoryList 
                    directories={ this.props.directories } 
                    removeDirectory={ this.props.removeDirectory } 
                    history={ this.props.history } />
                
                <AddDirectoryProjectForm 
                    handleSubmit={ this.props.addDirectory }
                />
            </div>
        )
    }
}


export default connect(mapStateToProps, mapDispatchToProps) (HomeView)