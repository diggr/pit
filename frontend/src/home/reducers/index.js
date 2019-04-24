const initialState = {
    loading: false,
    error: null,
    directories: []
}

const HomeReducer = (state=initialState, action) => {
    switch (action.type) {
        case 'FETCH_DIRECTORIES_BEGIN':
            return {
                ...state,
                loading: true,
                error: null,
                directories: []
            }
        case 'FETCH_DIRECTORIES_SUCCESS':
            return {
                ...state,
                loading: false,
                error: null, 
                directories: action.payload.directories
            }
        case 'FETCH_DIRECTORIES_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload.error,
                directories: []
            }
        case 'REMOVE_DIRECTORIES_BEGIN':
            return {
                ...state,
                loading: true
            }
        case 'REMOVE_DIRECTORIES_SUCCESS':
            return {
                ...state,
                loading: false,
                directories: action.payload.directories
            }
        case 'REMOVE_DIRECTORIES_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload.error,
                directories: []
            }
        case 'ADD_DIRECTORY_BEGIN':
            return {
                ...state,
                loading: true,
            }
        case 'ADD_DIRECTORY_SUCCESS':
            return {
                ...state,
                loading: false,
                directories: action.payload.directories
            }
        case 'ADD_DIRECTORY_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload.error,
                directories: []
            }
        default:
            return state
    }
} 

export default HomeReducer