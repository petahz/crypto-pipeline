import React from 'react';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';


export const Home = () => (
  <Table>
    <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
      <TableRow>
        <TableHeaderColumn>Name</TableHeaderColumn>
        <TableHeaderColumn>Bid/Ask Spread</TableHeaderColumn>
        <TableHeaderColumn>Relative Strength Indicator</TableHeaderColumn>
        <TableHeaderColumn>Trade Recommendation</TableHeaderColumn>
      </TableRow>
    </TableHeader>
    <TableBody displayRowCheckbox={false}>
      <TableRow>
        <TableRowColumn>Bitcoin</TableRowColumn>
        <TableRowColumn>20</TableRowColumn>
        <TableRowColumn>20</TableRowColumn>
        <TableRowColumn>Buy</TableRowColumn>
      </TableRow>
      <TableRow>
        <TableRowColumn>Ethereum</TableRowColumn>
        <TableRowColumn>65</TableRowColumn>
        <TableRowColumn>Neutral</TableRowColumn>
      </TableRow>
      <TableRow>
        <TableRowColumn>EOS</TableRowColumn>
        <TableRowColumn>88</TableRowColumn>
        <TableRowColumn>Sell</TableRowColumn>
      </TableRow>
      <TableRow>
        <TableRowColumn>Litecoin</TableRowColumn>
        <TableRowColumn>45</TableRowColumn>
        <TableRowColumn>Neutral</TableRowColumn>
      </TableRow>
      <TableRow>
        <TableRowColumn>Bitcoin Cash</TableRowColumn>
        <TableRowColumn>54</TableRowColumn>
        <TableRowColumn>Neutral</TableRowColumn>
      </TableRow>
    </TableBody>
  </Table>
);
