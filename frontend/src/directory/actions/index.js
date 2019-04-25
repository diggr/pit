export const fetchFileListBegin = () => ({
    type: 'FETCH_FILE_LIST_BEGIN'
})

export const fetchFileListSuccess = (fileList) => ({
    type: 'FETCH_FILE_LIST_SUCCESS',
    payload: { fileList }
}) 

export const fetchFileListError = (error) => ({
    type: 'FETCH_FILE_LIST_ERROR',
    payload: { error }
})

export const changeCurrentDirectory = (directory) => ({
    type: 'CHANGE_CURRENT_DIRECTORY',
    payload: { directory }
})

export const updateFileListBegin = () => ({
    type: 'UPDATE_FILE_LIST_BEGIN'
})

export const updateFileListSuccess = (fileList) => ({
    type: 'UPDATE_FILE_LIST_SUCCESS',
    payload: { fileList }
})

export const updateFileListError = (error) => ({
    type: 'UPDATE_FILE_LIST_ERROR',
    payload: { error }
})