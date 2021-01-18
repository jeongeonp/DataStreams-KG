import React, { Component } from 'react';
import './DagreKG.css';

import DagreGraph from 'dagre-d3-react'
import * as d3 from 'd3'

import relation from '../assets/rel_info.json'
import testdata from '../assets/test.json'
import result from '../assets/DocRED_result.json'

export class DagreKG extends Component {

    constructor(props) {
        super(props);
        
        this.state = {
            nodes: [],
            links: []
        }
        this.addNodes = this.addNodes.bind(this)
        this.addLinks = this.addLinks.bind(this)
        this.parseTestData = this.parseTestData.bind(this)
        this.parseResult = this.parseResult.bind(this)
        this.parseRelation = this.parseRelation.bind(this)
    }

    componentDidMount() {
        //this.parseTestData("Leon Crouch", 10)
        this.parseResult(100)

        //console.log(result)
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


    addNodes = (id, label, color = '#dddddd') => {
        var colorString = 'fill: ' + color
        var config = { style: colorString }
        var newNode = { id: id, label: label, labelType: "string", config: config }
        var currNodes = this.state.nodes
        currNodes.push(newNode)
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

    render() {
        const { nodes, links } = this.state
        return (
            <div>
                <DagreGraph
                    nodes={nodes}
                    links={links}
                    options={{
                        rankdir: 'TB',
                        align: 'UL',
                        ranker: 'tight-tree',
                        
                    }}
                    width='100%'
                    height='700'
                    animate={0}
                    shape='rect'
                    fitBoundaries
                    zoomable
                    onNodeClick={e => console.log(e)}
                    onRelationshipClick={e => console.log(e)}
                />
            </div>
        )
    }
}