export const fetchAgentsBegin = () => ({
    type: 'FETCH_AGENTS_BEGIN'
})

export const fetchAgentsSuccess = (agents) => ({
    type: 'FETCH_AGENTS_SUCCESS',
    payload: { agents }
})

export const fetchAgentsError = (error) => ({
    type: 'FETCH_AGENTS_ERROR',
    payload: { error }
})