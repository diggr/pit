import { fetchConfigBegin, fetchConfigSuccess, fetchConfigError } from '../actions'

export function fetchConfig () {
    return function (dispatch) {
        console.log("fetch config")
        dispatch(fetchConfigBegin())
        return fetch('http://localhost:5555/config')
            .then(res => res.json())
            .then(json => {
                console.log(json)
                dispatch(fetchConfigSuccess(json.config))
                return json.config
            })
        .catch( error => dispatch(fetchConfigError(error)))  
    }
} 