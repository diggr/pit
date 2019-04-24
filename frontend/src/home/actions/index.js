export const fetchDirectoriesBegin = () => ({
    type: 'FETCH_DIRECTORIES_BEGIN'
})

export const fetchDirectoriesSuccess = (directories)  => ({
    type: 'FETCH_DIRECTORIES_SUCCESS',
    payload: { directories }
})

export const fetchDirectoriesError = (error) => ({
    type: 'FETCH_DIRECTORIES_ERROR',
    payload: { error }
})

export const removeDirectoryBegin = () => ({
    type: 'REMOVE_DIRECTORY_BEGIN'
})

export const removeDirectorySuccess = (directories) => ({
    type: 'REMOVE_DIRECTORIES_SUCCESS',
    payload: { directories }
})

export const removeDirectoryError = (error) => ({
    type: 'REMOVE_DIRECTORY_ERROR',
    payload: { error }
})

export const addDirectoryBegin = () => ({
    type: 'ADD_DIRECTORY_BEGIN'
})

export const addDirectorySuccess = (directories) => ({
    type: 'ADD_DIRECTORY_SUCCESS',
    payload: { directories }
})

export const addDirectoryError = (error) => ({
    type: 'ADD_DIRECTORY_ERROR',
    payload: { error}
})