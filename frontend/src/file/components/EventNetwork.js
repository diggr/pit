import React, { Component } from 'react'
import { Network, DataSet } from 'vis'
import { withStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper'
import grey from '@material-ui/core/colors/grey'
// throws error if css is missing
import 'vis/dist/vis-timeline-graph2d.min.css'

const styles = theme => ({
    networkContainer: {
      width: '100%',
      height: 560
    },
    eventNetworkContainer: {
        marginTop: theme.spacing.unit * 8,
    },
    eventTimelineContainer: {
        width: '100%',
        height: 280
    },
    networkPaper: {
        marginRight: 30
    }
})

const lightCyan = '#4CB2D4';
const darkCyan = '#40A3C1';
const highlight = '#f1521a';
const sourceBlueGrey = grey['500'];

const getFilename = (location) => {
    return location.split("/").pop()
}

const generateLabel = (event) => {
    const { location, activity } = event
    const fileName = getFilename(location)
    const activitySplit = activity.split("/")
    const activitySlug = activitySplit[activitySplit.length - 2]
    return "<b>" + activitySlug + "</b>\n" + fileName 
}

const options = {
    layout: {
        improvedLayout: true,
        hierarchical: {
            sortMethod: "directed",
            levelSeparation: 120,

        }
    },
    edges: {
      smooth: true,
      arrows: {to : true },
      color: {
          color: darkCyan
      }
    },
    nodes: {    
        shape: 'box',
        shadow: true,
        font: {
            multi: true
        }
    },
    groups: {
        source: {
            font: {
                color: 'white',
            },
          color: {
            background: sourceBlueGrey,
            border: darkCyan,
            highlight: {
                background: highlight,
                border: '#EF5350'
            }
          }
        },
        file: {
            font: {
                color: 'white',
            },
            color: {
              background: darkCyan,
              border: lightCyan,
              highlight: {
                background: highlight,
                border: '#EF5350'
                }
            }
        },
        primarySource: {
            color: {
                background: '#ffffff',
            }
        }
    }
}
   
class EventNetwork extends Component {

    flatProvData (data) {
        this.provDict[data.uri] = data
        for (const source of data.sources) {
            this.flatProvData(source)
        }
    }

    iterProvData (root) {
        console.log(root.location)
        const currentNodes = this.nodes.getIds()
        const source = root.uri
        const filename = this.props.prov.location
        let group = 'source'
        if (root.location === filename)
            group = 'file'



        currentNodes.push(source)
        this.nodes.update({
            id: source,
            label: generateLabel(root),
            group: group,
            start: root.ended_at,
            content: generateLabel(root)
        })
    
        if (root.primary_sources) {
            for (const ps of root.primary_sources) {
                this.nodes.update({
                    id: ps,
                    label: "<i>Primary source</i>\n<b>"+getFilename(ps)+"</b>",
                    group: 'primarySource'
                })
                this.edges.update({
                    from: source,
                    to: ps,
                    arrows: 'from'
                })                
            }
        }
    
    
        if (root.sources) {
            for (const source_data of root.sources) {
                const target = source_data.uri
        
                const filename = this.props.prov.location
                let group = 'source'
                if (source_data.location === filename)
                    group = 'file'

                currentNodes.push(target)
                this.nodes.update({
                    id: target,
                    label: generateLabel(source_data),
                    group: group,
                    start: source_data.ended_at,
                    content: generateLabel(source_data)
                })
    
                this.edges.update({
                    from: source,
                    to: target,
                    arrows: 'from'
                })
            }
            for (const source_data of root.sources) {
                this.iterProvData(source_data)
            }
        }     
    }

    buildEdgeList (prov) {
        this.iterProvData(prov)
    }


    constructor (props) {
        super(props)
        this.nodes = new DataSet()
        this.edges = new DataSet()
    }


    isProvEvent (item) {
        let add = false
        this.nodes.forEach((node) => {
            if (node.id === item && node.group !== "primarySource") 
                add = true
        })
        return add
    }

    componentDidMount () {

        this.network = new Network(this.refs.eventNetwork, { nodes: this.nodes, edges: this.edges}, options)
        this.network.on("click", (event) => {
            const item = this.network.getNodeAt(event.pointer.DOM)
            if (this.isProvEvent(item)) 
                this.props.changeProvEvent(item)
            else
                this.props.changeProvEvent("")
        })
    }

    componentDidUpdate () {
        const { prov, currentProvEvent, updateNetwork, rebuildNetwork, networkUpdated } = this.props

        if (rebuildNetwork) {
            // console.log("rebuilding network")
            // this.network.destroy()
            // this.nodes = new DataSet()
            // this.edges = new DataSet()
            // this.network = new Network(this.refs.eventNetwork, { nodes: this.nodes, edges: this.edges}, options)
            const currentNodes = this.nodes.getIds()
            for (const nodeId of currentNodes)
                this.nodes.remove(nodeId)     
            const currentEdges = this.edges.getIds()     
            for (const edgeId of currentEdges)  
                this.edges.remove(edgeId)

            this.buildEdgeList(prov)

        }

        if (! (Object.keys(prov).length === 0 && prov.constructor === Object) && updateNetwork) {
            console.log("add update")
            this.buildEdgeList(prov)
            networkUpdated()
        }

        if (currentProvEvent !== "" && currentProvEvent)
            this.network.selectNodes( [currentProvEvent] )
        else
            this.network.selectNodes( [] )            

    }

    render () {
        const { classes } = this.props
        return (
            <div>
                <Paper className={ classes.networkPaper }>
                    <div className={ classes.networkContainer } ref="eventNetwork"></div>  
                </Paper>
            </div>
        )
    }
}

export default withStyles(styles) (EventNetwork)