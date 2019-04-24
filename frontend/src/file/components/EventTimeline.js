import React, { Component } from 'react'
import { Timeline, DataSet } from 'vis'
import { withStyles } from '@material-ui/core/styles'
// throws error if css is missing
import 'vis/dist/vis-timeline-graph2d.min.css'
import './EventTimeline.css'

const styles = theme => ({
    eventTimelineContainer: {
        width: '100%',
        height: 280
    }
})

const getFilename = (location) => {
    return location.split("/").pop()
}

const generateLabel = (event) => {
    const { activity } = event
    const activitySplit = activity.split("/")
    const activitySlug = activitySplit[activitySplit.length - 2]
    return activitySlug
}


class EventTimeline extends Component {

    constructor (props) {
        super(props)
        this.nodes = new DataSet()
    }


    iterProvData (root) {

        const currentNodes = this.nodes.getIds()

        const source = root.uri
        
        if (root.started_at)
            this.nodes.update({
                id: source,
                label: generateLabel(root),
                group: getFilename(root.location),
                start: root.started_at,
                end: root.ended_at,
                content: generateLabel(root)
            })
        else
            this.nodes.update({
                id: source,
                label: generateLabel(root),
                group: getFilename(root.location),
                start: root.ended_at,
                content: generateLabel(root)
            })

        currentNodes.push(source)

    
        
        if (root.sources) {
            for (const source_data of root.sources) {
                const target = source_data.uri
    

    
                    currentNodes.push(target)
                    this.nodes.update({
                        id: target,
                        label: generateLabel(source_data),
                        group: getFilename(source_data.location),
                        start: source_data.ended_at,
                        content: generateLabel(source_data),
                    })


            }
            for (const source_data of root.sources) {
                this.iterProvData(source_data)
            }
        }     
    }


    componentDidMount () {

        const options = {
            verticalScroll: true,
            maxHeight: 250
        }

        this.timeline = new Timeline(this.refs.eventTimeline, this.nodes, options)
        this.timeline.on("click", (event) => {
            const item = event.item           
            this.props.changeProvEvent(item)
            this.timeline.on("click", (event) => {
                const item = event.item            
                this.props.changeProvEvent(item)
            })               
        })          
    }

    componentDidUpdate () {
        const { prov, currentProvEvent } = this.props
        console.log("pudate timeline start")


        const currentIds = this.nodes.getIds()
        for (const nodeId of currentIds)
            this.nodes.remove(nodeId)
            


        if (! (Object.keys(prov).length === 0 && prov.constructor === Object) ) { 
            console.log("update timeline")


            
            console.log(this.nodes)
            this.iterProvData(prov)

            if (this.nodes.length === 0) {
                //if this.
                //this.timeline.destroy()
            }
            else {
                const allGroups = this.nodes.map( (node,i ) => node.group )
                const group = []
                const done = []
                for (const i in allGroups) {
                    if (done.indexOf(allGroups[i]) < 0) {
                        group.push({
                            id: allGroups[i], 
                            content: allGroups[i] 
                        })
                        done.push(allGroups[i])
                    }
                }
                this.timeline.setGroups(group)
                this.timeline.fit()       
            }
        }
        if (currentProvEvent)
            this.timeline.setSelection(currentProvEvent)  
        else
            this.timeline.setSelection("")
    }


    render () {
        const { classes } = this.props
        return (
            <div>
                <div className={ classes.eventTimelineContainer } ref="eventTimeline"></div>  
            </div>
        )
    }

}

export default withStyles(styles) (EventTimeline)