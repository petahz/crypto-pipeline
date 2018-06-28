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
        const mapper = {
            'XXBTZUSD': 'Bitcoin',
            'XETHZUSD': 'Ethereum',
            'EOSUSD': 'EOS',
            'XLTCZUSD': 'Litecoin',
            'BCHUSD': 'Bitcoin Cash'
        };
        
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
                <TableBody if={this.props.liveData} displayRowCheckbox={false}>
                    { Object.keys(this.props.liveData).map((assetPair, index) => {
                        const values = this.props.liveData[assetPair];
                        return (<TableRow key={index} if={mapper[assetPair]}>
                            <TableRowColumn>{mapper[assetPair]}</TableRowColumn>
                            <TableRowColumn>{values && values.bid}</TableRowColumn>
                            <TableRowColumn>{values && values.ask}</TableRowColumn>
                            <TableRowColumn>{values && values.spread}</TableRowColumn>
                            <TableRowColumn>{values && values.avg_spread}</TableRowColumn>
                        </TableRow>)
                    }) }
                </TableBody>
            </Table>
        )
    }
}
