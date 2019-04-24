const initialState = {
    currentDirectory: null,
    fileList: [],
    loading: false,
    error: null,
}

const DirectoryReducer = (state=initialState, action) => {
    switch (action.type) {
        case 'FETCH_FILE_LIST_BEGIN':
            return {
                ...state,
                loading: true,
                error: null
            }
        case 'FETCH_FILE_LIST_SUCCESS':
            return {
                ...state,
                loading: false,
                fileList: action.payload.fileList
            }
        case 'FETCH_FILE_LIST_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload.error,
                fileList: []
            }
        case 'CHANGE_CURRENT_DIRECTORY':
            return {
                ...state,
                currentDirectory: action.payload.directory
            }
        case 'UPDATE_FILE_LIST_BEGIN':
            return {
                ...state,
                loading: true,
                error: null
            }
        case 'UPDATE_FILE_LIST_SUCCESS':
            return {
                ...state,
                loading: false,
                fileList: action.payload.fileList
            }
        default:
            return state
    }
}

export default DirectoryReducer