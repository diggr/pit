export const fetchConfigBegin = () => ({
    type: 'FETCH_CONFIG_BEGIN'
})

export const fetchConfigSuccess = (config) => ({
    type: 'FETCH_CONFIG_SUCCESS',
    payload: { config }
})

export const fetchConfigError = (error) => ({
    type: 'FETCH_CONFIG_ERROR',
    payload: { error }
})

export const updateProvitDir = (provitDir) => ({
    type: 'UPDATE_PROVIT_DIR',
    payload: { provitDir }
})