const initialState = {
    provitDir: "",
    loading: false,
    error: null,
    changed: false
}

const ConfigReducer = ( state = initialState, action) => {
    switch (action.type) {
        case 'FETCH_CONFIG_BEGIN':
            return {
                ...state,
                loading: true,
                error: null
            }
        case 'FETCH_CONFIG_SUCCESS':
            return {
                ...state,
                loading: false,
                provitDir: action.payload.config.provit_dir
            }
        case 'FETCH_CONFIG_ERROR':
            return {
                ...state,
                loading: false,
                provitDir: "",
                error: action.payload.error
            }
        case 'UPDATE_PROVIT_DIR':
            return {
                ...state,
                changed: true,
                provitDir: action.payload.provitDir
            }
        default:
            return state
    }
}

export default ConfigReducer