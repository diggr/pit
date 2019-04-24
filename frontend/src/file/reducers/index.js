const initalState = {
    prov: {},
    agents: [],
    hasProv: false,
    currentFile: "",
    currentProvEvent: "",
    loading: false,
    error: null,
    updateNetwork: false,
    rebuildNetwork: false,
    rebuildTimeline: false,
    currentAgent: "",
    showAgentDialog: false,
    showAddProvForm: false
}

const FileReducer = (state=initalState, action) => {
    switch (action.type) {
        case 'FETCH_PROV_BEGIN':
            return {
                ...state,
                prov: {},
                agent: [],
                currentFile: "",
                currentProvEvent: "",
                currentAgent: "",
                showAgentDialog: false,
                loading: true,
                error: null
            }
        case 'FETCH_PROV_SUCCESS':
            console.log(action.payload)
            return {
                ...state,
                hasProv: action.payload.data.hasProv,
                prov: action.payload.data.prov,
                agents: action.payload.data.agents,
                currentProvEvent: action.payload.data.prov.uri,
                loading: false,
                updateNetwork: true
            }
        case 'FETCH_PROV_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload.error
            }
        case 'ADD_PROV_BEGIN': 
            return {
                showAddProvForm: false,
                prov: {},
                agent: [],
                currentFile: "",
                currentProvEvent: "",
                currentAgent: "",
                showAgentDialog: false,                
                loading: true,
                error: null
            }
        case 'ADD_PROV_SUCCESS':
            return {
                ...state,
                loading: false,
                hasProv: action.payload.data.hasProv,
                prov: action.payload.data.prov,
                currentFile: action.payload.data.prov.location,
                agents: action.payload.data.agents,
                currentProvEvent: action.payload.data.prov.uri,
                updateNetwork: true,
                rebuildNetwork: true            
            }
        case 'REMOVE_PROV_BEGIN':
            return {
                showAddProvForm: false,
                prov: {},
                agent: [],
                //currentFile: "",
                currentProvEvent: "",
                currentAgent: "",
                showAgentDialog: false,                
                loading: true,
                error: null,
            }        
        case 'REMOVE_PROV_SUCCESS':
            console.log(action.payload)
            return {
                ...state,
                loading: false,
                hasProv: action.payload.data.hasProv,
                prov: action.payload.data.prov,
                //currentFile: "",
                agents: action.payload.data.agents,
                currentProvEvent: "",
                updateNetwork: true,
                rebuildNetwork: true,             
            }        
        case 'CHANGE_CURRENT_FILE':
            return {
                ...state,
                currentFile: action.payload.currentFile
            }
        case 'CHANGE_PROV_EVENT':
            return {
                ...state,
                currentProvEvent: action.payload.currentProvEvent
            }
        case 'NETWORK_UPDATED':
            return {
                ...state,
                updateNetwork: false,
                rebuildNetwork: false
            }
        case 'SET_CURRENT_AGENT':
            return {
                ...state,
                currentAgent: action.payload.currentAgent,
                showAgentDialog: true
            }
        case 'HIDE_AGENT_DIALOG':
            return {
                ...state,
                showAgentDialog: false
            }   
        case 'TOGGLE_ADD_PROV_FORM':
            return {
                ...state,
                showAddProvForm: !state.showAddProvForm
            }
        case 'RESET_FILE_STATE':
            return initalState
        default:
            return state
    }
}

export default FileReducer