import { fetchAgentsBegin, fetchAgentsSuccess, fetchAgentsError } from '../actions'

export function fetchAgents () {
    return function (dispatch) {
        console.log("fetch agents")
        dispatch(fetchAgentsBegin())
        return fetch('http://localhost:5555/agents')
            .then(res => res.json())
            .then(json => {
                console.log(json)
                dispatch(fetchAgentsSuccess(json.agents))
                return json.agents
            })
        .catch( error => dispatch(fetchAgentsError(error)))  
    }
} 