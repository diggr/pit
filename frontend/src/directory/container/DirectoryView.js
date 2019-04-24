import React, { Component } from 'react'
import { connect } from 'react-redux'
import * as api from '../api'
import * as actions from '../actions'
import FileTable from '../components/FileTable'




const mapStateToProps = (state) => ({
    fileList: state.directory.fileList,
    currentDirectory: state.directory.currentDirectory
}) 

const mapDispatchToProps = {
    fetchFileList: api.fetchFileList,
    changeCurrentDirectory: actions.changeCurrentDirectory,
    updateFileList: api.updateFiles
}


class DirectoryView extends Component {

    componentDidMount () {
        const directory = this.props.location.search.substr(1)
        console.log(directory)
        this.props.fetchFileList(directory)
        this.props.changeCurrentDirectory(directory)
    }

    componentDidUpdate () {
        // fetch file list if location search path is changed
        const directory = this.props.location.search.substr(1)
        if (directory !== this.props.currentDirectory) {
            this.props.fetchFileList(directory)
            this.props.changeCurrentDirectory(directory)        
        }
    }

    render () {
        return (
            <div>

                <FileTable 
                    fileList={this.props.fileList} 
                    history={this.props.history} 
                    directory={this.props.currentDirectory} 
                    updateFileList={this.props.updateFileList}
                />
            </div>
        )
    }
} 

export default connect(mapStateToProps, mapDispatchToProps) (DirectoryView)