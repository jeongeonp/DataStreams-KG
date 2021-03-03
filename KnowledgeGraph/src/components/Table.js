import React, { Component } from 'react';
import { Icon, Label, Menu, Table } from 'semantic-ui-react'
// import { CsvToHtmlTable } from 'react-csv-to-table';
// import sampleData from './assets/paper_info/nilm_100_exact_author_expertise.csv'
// import jsonData from './assets/paper_info/nilm_100_exact_author_knowledge';
import jsonData from '../assets/ScholarTable.json';



const ScholarTable = ({filterIndex}) => {
  console.log("filterIndex ", filterIndex)
  console.log("jsonData ",  jsonData[filterIndex]);
  // console.log(Object.entries(jsonData));
  var wholeArray = Object.keys(jsonData[filterIndex]).map(key => jsonData[filterIndex][key]);
  wholeArray.sort(function(a,b) {
    return b.Citations - a.Citations
  })


  console.log("wholeArray ", wholeArray);
    return (
      <div>
        <Table celled compact>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell> Author </Table.HeaderCell>
            <Table.HeaderCell> Title </Table.HeaderCell>
            {/* <Table.HeaderCell> Rank </Table.HeaderCell> */}
            <Table.HeaderCell> Citations </Table.HeaderCell>
            <Table.HeaderCell> Year </Table.HeaderCell>
            <Table.HeaderCell> Source </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
        {wholeArray.map((item, i) => {
          return (
          <Table.Row>
            <Table.Cell> {item['Author']} </Table.Cell>
            <Table.Cell> {item['Title']} </Table.Cell>
            {/* <Table.Cell> {item['Rank']} </Table.Cell> */}
            <Table.Cell> {item['Citations']} </Table.Cell>
            <Table.Cell> {item['Year']} </Table.Cell>
            <Table.Cell> <a href={item['Source']}> link </a> </Table.Cell>
          </Table.Row>)
        })}
        </Table.Body>
        </Table>
      </div>
    );
}

export default ScholarTable;
