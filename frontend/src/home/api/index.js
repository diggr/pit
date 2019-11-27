import { 
    fetchDirectoriesBegin, fetchDirectoriesSuccess, fetchDirectoriesError,
    removeDirectoryBegin, removeDirectorySuccess, removeDirectoryError,
    addDirectoryBegin, addDirectorySuccess, addDirectoryError
 } from '../actions'

export function fetchDirectories () {
    return function (dispatch) {
        console.log("fetch directories")
        dispatch(fetchDirectoriesBegin())
        return fetch('http://localhost:5555/directories')
            .then(res => res.json())
            .then(json => {
                dispatch(fetchDirectoriesSuccess(json.directories))
                return json.directories
            })
        .catch( error => dispatch(fetchDirectoriesError(error)))  
    }
} 

export function removeDirectory (directory) {
    return function (dispatch) {
        console.log("remove directory "+directory)
        dispatch(removeDirectoryBegin())
        return fetch('http://localhost:5555/directories/remove',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },            
            mode: 'cors',
            body: JSON.stringify({ directory })
            })
            .then(res => res.json())
            .then(json => {
                dispatch(removeDirectorySuccess(json.directories))
                return json.directories
            })
            .catch(error => dispatch(removeDirectoryError(error)))
    }
}

export function addDirectory (directory) {
    return function (dispatch) {
        console.log("add directory "+directory)
        dispatch(addDirectoryBegin())
        return fetch('http://localhost:5555/directories',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
             },            
            mode: 'cors',
            body: JSON.stringify({ directory })
            })
            .then(res => res.json())
            .then(json => {
                dispatch(addDirectorySuccess(json.directories))
                return json.directories
            })
            .catch(error => dispatch(addDirectoryError(error)))
    }
}