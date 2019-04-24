import React, { Component } from 'react'
import { Provider } from 'react-redux'
import store from './store'
import './App.css'

import { BrowserRouter as Router, Route, Switch} from 'react-router-dom'

import Typography from '@material-ui/core/Typography'


import ConfigView from './config/container/ConfigView'
import HomeView from './home/container/HomeView'
import DirectoryView from './directory/container/DirectoryView'
import AgentListView from './agents/container/AgentListView'
import FileView from './file/container/FileView'

import Menu from './Menu'

import CssBaseline from '@material-ui/core/CssBaseline'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles'

const theme = createMuiTheme({
    palette: {
      primary: {
        light: '#B4E1FF',
        main: '#4CB2D4',
        dark: '#40A3C1',
        contrastText: '#fff',
      },
      secondary: {
        light: '#FF964E',
        main: '#EB7B2D',
        dark: '#f1521a',
        contrastText: '#fff',
      },
    },
  })
  

class App extends Component {


  render() {
    return (
      <Provider store={store}>
        <CssBaseline />
        <MuiThemeProvider theme={theme}>
          <div className="App">
            <header className="App-header">
              <Typography component="h2" variant="display1">provit</Typography>
            </header>

            <Router>
              <div>

                <Menu />

                <Switch>
                  <Route exact path="/" component={ HomeView } />
                  <Route path="/config" component={ ConfigView } />
                  <Route path="/directory" component={ DirectoryView } />
                  <Route path="/agents" component={ AgentListView } />
                  <Route path="/file" component={ FileView } />
                </Switch>
              </div>
            </Router>
          </div>

        </MuiThemeProvider>
      </Provider>
    )
  }
}

export default App
