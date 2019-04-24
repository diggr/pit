import { 
    fetchProvBegin, fetchProvSuccess, fetchProvError,
    addProvBegin, addProvSuccess, addProvError,
    removeProvBegin, removeProvSuccess, removeProvError
} from '../actions'

export function fetchProv (filepath) {
    return function (dispatch) {
        console.log("fetch prov information")
        dispatch(fetchProvBegin())
        return fetch('http://localhost:5555/file',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },            
            mode: 'cors',
            body: JSON.stringify({ filepath })
            })
            .then(res => res.json())
            .then(json => {
                console.log(json)
                dispatch(fetchProvSuccess(json))
                return json.prov
            })
            .catch(error => dispatch(fetchProvError(error)))
    }
} 

export function addProv (filepath, prov, isTimestamp) {
    return function (dispatch) {
        console.log("add prov information")
        console.log(isTimestamp)
        dispatch(addProvBegin())
        return fetch('http://localhost:5555/file/add',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },            
            mode: 'cors',
            body: JSON.stringify({ filepath, prov, isTimestamp })
            })
            .then(res => res.json())
            .then(json => {
                console.log(json)
                dispatch(addProvSuccess(json))
                return json.prov
            })
            .catch(error => dispatch(addProvError(error)))
    }
} 

export function removeProv (filepath) {
    return function (dispatch) {
        console.log("remove prov information")
        dispatch(removeProvBegin())
        return fetch('http://localhost:5555/file/remove',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },            
            mode: 'cors',
            body: JSON.stringify({ filepath })
            })
            .then(res => res.json())
            .then(json => {
                console.log(json)
                dispatch(removeProvSuccess(json))
                return json.prov
            })
            .catch(error => dispatch(removeProvError(error)))
    }
} 