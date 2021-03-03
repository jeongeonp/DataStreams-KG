import React, { Component } from 'react';
import './D3KG.css';

import { Graph } from "react-d3-graph";
import * as d3 from 'd3'
import { Grid, Image, Input, Icon, Segment } from "semantic-ui-react"
import ScholarTable from './Table';


import relation from '../assets/rel_info.json'
import testdata from '../assets/test.json'
import traindata from '../assets/train_annotated.json'
import result from '../assets/DocRED_result.json'
import subgraph from '../assets/subgraph.json'



// graph event callbacks
const onClickGraph = function() {
    window.alert(`Clicked the graph background`);
};

const onClickNode = function(nodeId) {
    window.alert(`Clicked node ${nodeId}`);
};

const onDoubleClickNode = function(nodeId) {
    window.alert(`Double clicked node ${nodeId}`);
};

const onRightClickNode = function(event, nodeId) {
    window.alert(`Right clicked node ${nodeId}`);
};

const onMouseOverNode = function(nodeId) {
    window.alert(`Mouse over node ${nodeId}`);
};

const onMouseOutNode = function(nodeId) {
    window.alert(`Mouse out node ${nodeId}`);
};

const onClickLink = function(source, target) {
    window.alert(`Clicked link between ${source} and ${target}`);
};

const onRightClickLink = function(event, source, target) {
    window.alert(`Right clicked link between ${source} and ${target}`);
};

const onMouseOverLink = function(source, target) {
    window.alert(`Mouse over in link between ${source} and ${target}`);
};

const onMouseOutLink = function(source, target) {
    window.alert(`Mouse out link between ${source} and ${target}`);
};

const onNodePositionChange = function(nodeId, x, y) {
    console.log(`Node ${nodeId} is moved to new position. New position is x= ${x} y= ${y}`);
};

export default class D3Tree extends React.Component {

    constructor(props) {
        super(props);
        
        this.state = {
            nodes: [],
            links: [],
            data: {},
            currentNode: subgraph['nodes'][0]['id'],
        }
        this.addNodes = this.addNodes.bind(this)
        this.addLinks = this.addLinks.bind(this)
        this.parseTestData = this.parseTestData.bind(this)
        this.parseResult = this.parseResult.bind(this)
        this.parseRelation = this.parseRelation.bind(this)
        this.parseSubgraph = this.parseSubgraph.bind(this)

        this.clickNode = this.clickNode.bind(this)
    }

    componentDidMount() {
        //this.parseTrainData()
        // this.parseResult(10)
        this.parseSubgraph()
    }

    componentDidUpdate(prevProps, prevState) {
        const { nodes, links } = this.state
        if (prevState.nodes !== this.state.nodes || prevState.links !== this.state.links) {
            this.setState({nodes: nodes, links: links})
            console.log(this.state.data)
        }
        
    }

    parseTestData(title, index) {
        const vertexSet = testdata.filter(v => v['title'] === title)[0]['vertexSet']
        //console.log(vertexSet[index][0]['name'])
        return vertexSet[index][0]['name']
    }

    parseResult(num) {
        for (var i in result.slice(0, num)) {
            const sour = this.parseTestData(result[i]['title'], result[i]['h_idx'])
            const dest = this.parseTestData(result[i]['title'], result[i]['t_idx'])
            const rel = this.parseRelation(result[i]['r'])
            this.addNodes(sour, sour)
            this.addNodes(dest, dest)
            this.addLinks(sour, dest, rel, rel)
        }
    }

    parseRelation(key) {
        //console.log(relation[key])
        return relation[key]
    }

    parseSubgraph() {
      console.log(subgraph)
      this.setState({nodes: subgraph['nodes'], links: subgraph['links']})
    }

    parseTrainData() {
        const labels = traindata.map(v => v['labels'].length)
        var temp = 0
        for (var l in labels) {
            temp += labels[l]
        }
        console.log(temp/traindata.length)

        // console.log(traindata.filter(v => v['title'] === "Short-beaked common dolphin")[0])
        // console.log(traindata.filter(v => v['title'] === "AirAsia Zest")[0])
        // console.log(traindata.filter(v => v['title'] === "AirAsia Zest")[0]['labels'])
        // console.log(traindata.filter(v => v['title'] === "AirAsia Zest")[0]['vertexSet'].map(v => v[0]['name']))
        // console.log(traindata.filter(v => v['title'] === "AirAsia Zest")[0]['sents'].map(v => v.join(" ")))
        
    }


    addNodes = (id, label, color = '#555555') => {
        var colorString = 'fill: ' + color
        var config = { style: colorString }
        var newNode = { id: id,  }
        var currNodes = this.state.nodes
        if (this.state.nodes.map(v => v.id).indexOf(id) === -1) {
            currNodes.push(newNode)
            console.log("*", id)
        }
        this.setState({
            nodes: currNodes
        })
    }

    addLinks = (source, target, label, id) => {
        var newLink = { source: source, target: target, label: label, config: {curve: d3.curveBasis, labelStyle: 'font-size: 65%; color: blue'}}
        var currLinks = this.state.links
        currLinks.push(newLink)
        this.setState({
            links: currLinks,
        })
    }

    clickNode = function(nodeId) {
        //window.alert(`Clicked node ${nodeId}`);
        console.log(nodeId)
        this.setState({
            currentNode: nodeId
        })
    }

    render() {
        const { nodes, links, data, currentNode } = this.state
        // console.log("this.state ", this.state)
        const { clickNode } = this
        //const data = {nodes: [{id: 'sally'}, {id: 'tom'}], links: [{source: 'sally', target: 'tom'}]}
        const myConfig = {
            automaticRearrangeAfterDropNode: false,
            nodeHighlightBehavior: true,
            //renderLabel: true,
            maxZoom: 8,
            minZoom: 0.01,
            width: 1400,
            height: 700,
            collapsible: false,
            staticGraphWithDragAndDrop: false,
            highlightDegree: 1,
            highlightOpacity: 1,
            directed: true,
            d3: {
                gravity: -1000,
                linkLength: 100000,
                // disableLinkForce: true,
            },
            node: {
                color: "lightblue",
                highlightColor: "#2a9df4",
                highlightFontSize: 14,
                size: 1200,
                highlightStrokeColor: "#2a9df4",
                fontSize: 24,
                labelPosition: "center",
                opacity: 0.8,
            },
            link: {
                highlightColor: "#2a9df4",
                renderLabel: true,
                color: "grey",
                fontSize: 24,
                opacity: 0.8,
                labelProperty: "label",
            },
        };
        
        return (
            <>
            <Grid style={{border: '5px solid white', height: '100%'}}>
                <Grid.Row>
                    <Grid.Column style={{paddingTop: '10px', marginLeft: '10px'}} width={15}>
                        <h2>Knowledge Graph</h2>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={12}>
                        <div style={{border: '2px solid grey', background: '#eeeeee'}}>
                        { nodes.length > 0 && links.length > 0 ?
                            <Graph
                                id="graph"
                                data={{nodes: nodes, links: links}}
                                config={myConfig}
                                onClickNode={clickNode}
                                
                                /*
                                onDoubleClickNode={onDoubleClickNode}
                                onRightClickNode={onRightClickNode}
                                onClickGraph={onClickGraph}
                                onClickLink={onClickLink}
                                onRightClickLink={onRightClickLink}
                                onMouseOverNode={onMouseOverNode}
                                onMouseOutNode={onMouseOutNode}
                                onMouseOverLink={onMouseOverLink}
                                onMouseOutLink={onMouseOutLink}
                                onNodePositionChange={onNodePositionChange}
                                */
                            />
                            :
                            <div>"No data yet"</div>
                        }
                        </div>
                    </Grid.Column>
                    <Grid.Column width={4}>
                        <div style={{padding: '0px'}}>
                            <Input
                            icon={<Icon name='search' inverted circular link />}
                            placeholder='Search...'
                            /> 
                            <div style={{padding:'10px'}}></div>
                            <div><h1> Current Node: {currentNode}</h1></div>  
                        </div>
                        
                    </Grid.Column>
                </Grid.Row>
            </Grid>
            <ScholarTable filterIndex = {this.state.currentNode}/>
            
            </>
        )
    }
}