import React from 'react';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';

/* components */
import { CoinRow } from '../CoinRow';


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
                    { Object.keys(mapper).map((assetPair, index) => {
                        const values = this.props.liveData[assetPair];
                        if (typeof(values) !== 'undefined') {
                            return (<CoinRow key={index} coinName={mapper[assetPair]} values={values}/>)
                        }
                    }) }
                </TableBody>
            </Table>
        )
    }
}
