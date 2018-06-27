import React from 'react';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';


export class Home extends React.Component {
    render() {
        return (
            <Table>
                <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
                    <TableRow>
                        <TableHeaderColumn>Name</TableHeaderColumn>
                        <TableHeaderColumn>Bid</TableHeaderColumn>
                        <TableHeaderColumn>Ask</TableHeaderColumn>
                        <TableHeaderColumn>Avg Spread</TableHeaderColumn>
                    </TableRow>
                </TableHeader>
                <TableBody displayRowCheckbox={false}>
                    <TableRow>
                        <TableRowColumn>Bitcoin</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'].spread}</TableRowColumn>
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
        )
    }
}
