export const fetchProvBegin = () => ({
    type: 'FETCH_PROV_BEGIN'
})

export const fetchProvSuccess = (data) => ({
    type: 'FETCH_PROV_SUCCESS',
    payload: { data }
})

export const fetchProvError = (error) => ({
    type: 'FETCH_PROV_ERROR',
    payload: { error }
})

export const addProvBegin = () => ({
    type: 'ADD_PROV_BEGIN'
})

export const addProvSuccess = (data) => ({
    type: 'ADD_PROV_SUCCESS',
    payload: { data }
})

export const addProvError = (error) => ({
    type: 'ADD_PROV_ERROR',
    payload: { error }
})

export const removeProvBegin = () => ({
    type: 'REMOVE_PROV_BEGIN',
})

export const removeProvSuccess = (data) => ({
    type: 'REMOVE_PROV_SUCCESS',
    payload: { data }
})

export const removeProvError = (error) => ({
    type: 'REMOVE_PROV_ERROR',
    payload: { error }
})

export const changeCurrentFile = (currentFile) => ({
    type: 'CHANGE_CURRENT_FILE',
    payload: { currentFile }
})

export const changeProvEvent = (currentProvEvent) => ({
    type: 'CHANGE_PROV_EVENT',
    payload: { currentProvEvent }
})

export const networkUpdated = () => ({
    type: 'NETWORK_UPDATED'
})

export const setCurrentAgent = (currentAgent) => ({
    type: 'SET_CURRENT_AGENT',
    payload: { currentAgent }
})

export const hideAgentDialog = (agentDialog) => ({
    type: 'HIDE_AGENT_DIALOG'
})

export const toggleAddProvForm = () => ({
    type: 'TOGGLE_ADD_PROV_FORM'
})

export const resetFileState = () => ({
    type: 'RESET_FILE_STATE'
})