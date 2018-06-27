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
                        <TableHeaderColumn>Current Spread</TableHeaderColumn>
                        <TableHeaderColumn>Avg Spread</TableHeaderColumn>
                    </TableRow>
                </TableHeader>
                <TableBody displayRowCheckbox={false}>
                    <TableRow>
                        <TableRowColumn>Bitcoin</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'] && this.props.liveData['XXBTZUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'] && this.props.liveData['XXBTZUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'] && this.props.liveData['XXBTZUSD'].spread}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XXBTZUSD'] && this.props.liveData['XXBTZUSD'].avg_spread}</TableRowColumn>
                    </TableRow>
                    <TableRow>
                        <TableRowColumn>Ethereum</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XETHZUSD'] && this.props.liveData['XETHZUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XETHZUSD'] && this.props.liveData['XETHZUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XETHZUSD'] && this.props.liveData['XETHZUSD'].spread}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XETHZUSD'] && this.props.liveData['XETHZUSD'].avg_spread}</TableRowColumn>
                    </TableRow>
                    <TableRow>
                        <TableRowColumn>EOS</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['EOSUSD'] && this.props.liveData['EOSUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['EOSUSD'] && this.props.liveData['EOSUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['EOSUSD'] && this.props.liveData['EOSUSD'].spread}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['EOSUSD'] && this.props.liveData['EOSUSD'].avg_spread}</TableRowColumn>
                    </TableRow>
                    <TableRow>
                        <TableRowColumn>Litecoin</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XLTCZUSD'] && this.props.liveData['XLTCZUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XLTCZUSD'] && this.props.liveData['XLTCZUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XLTCZUSD'] && this.props.liveData['XLTCZUSD'].spread}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['XLTCZUSD'] && this.props.liveData['XLTCZUSD'].avg_spread}</TableRowColumn>
                    </TableRow>
                    <TableRow>
                        <TableRowColumn>Bitcoin Cash</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['BCHUSD'] && this.props.liveData['BCHUSD'].bid}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['BCHUSD'] && this.props.liveData['BCHUSD'].ask}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['BCHUSD'] && this.props.liveData['BCHUSD'].spread}</TableRowColumn>
                        <TableRowColumn>{this.props.liveData['BCHUSD'] && this.props.liveData['BCHUSD'].avg_spread}</TableRowColumn>
                    </TableRow>
                </TableBody>
            </Table>
        )
    }
}
