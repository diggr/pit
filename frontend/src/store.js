import {createStore, combineReducers, applyMiddleware} from 'redux'
import thunk from 'redux-thunk'

import ConfigReducer from './config/reducers'
import HomeReducer from './home/reducers'
import DirectoryReducer from './directory/reducers'
import AgentsReducer from './agents/reducers'
import FileReducer from './file/reducers'

import { createForms } from 'react-redux-form'
import AddProvFormReducer from './forms/reducers/AddProvFormReducer'
import AddProjectDirectoryFormReducer from './forms/reducers/AddProjectDirectoryFormReducer'

const reducers = combineReducers({
    home: HomeReducer,
    config: ConfigReducer,
    directory: DirectoryReducer,
    agents: AgentsReducer,
    file: FileReducer,
    ...createForms({
        addProjectDirectory: AddProjectDirectoryFormReducer,
        addProvEvent: AddProvFormReducer,
        })
    })

const store = createStore(
    reducers,
    applyMiddleware(thunk)
)

export default store