import { 
    fetchFileListBegin, fetchFileListSuccess, fetchFileListError,
    updateFileListBegin, updateFileListSuccess, updateFileListError
 } from '../actions'


export function fetchFileList (directory) {
    return function (dispatch) {
        console.log("fetch filelist")
        dispatch(fetchFileListBegin())
        return fetch('http://localhost:5555/directory',{
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
                console.log(json)
                dispatch(fetchFileListSuccess(json.files))
                return json.files
            })
            .catch(error => dispatch(fetchFileListError(error)))
    }
} 

export function updateFiles (directory) {
    return function (dispatch) {
        console.log("update filelist")
        dispatch(updateFileListBegin())
        return fetch('http://localhost:5555/directory/update',{
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
                console.log(json)
                dispatch(updateFileListSuccess(json.files))
                return json.files
            })
            .catch(error => dispatch(updateFileListError(error)))
    }
} 