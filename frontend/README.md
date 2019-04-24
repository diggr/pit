# Provit Frontend

Basic browser based frontend for provit provenance information.

* Allows to view all directories in the provit setup.
* Manages provit configuration
* See agent profiles
* Visual representation of provit provenance graphs 
* Add new prov events, delete last prov event



## Provit Version 1.0 Todo:


- [ ] Allow to set timestamp when adding new prov event (at the moment, current time is used as a default value)
- [ ] Use file picker component for config form (= build decent config form!)
- [ ] Build forms for adding / changing agents
- [ ] Support line breaks in event descriptions
- [ ] Shorten long filenames
- [ ] Test compatibility to Windows and Mac 
- [ ] Add help page
- [x] Allow to define start and stop time for a new prov event
- [ ] Add a field for primary soruces in the event details
- [ ] Allow clustering of source file prov events in the network in order to improve readability
- [ ] Allow different network layouts




This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

This project uses vis.js for timeline and network visualization.
Forms are build with the help of react-redux-forms.