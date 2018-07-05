import React from 'react';
import {
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';


let changes = {
    bid: false,
    ask: false,
    avg_spread: false,
};

export class CoinRow extends React.Component {
    componentWillReceiveProps(nextProps) {
        changes = {
            bid: false,
            ask: false,
            avg_spread: false,
        };

        if (this.props.values.bid !== nextProps.values.bid) {
            changes.bid = true;
        }

        if (this.props.values.ask !== nextProps.values.ask) {
            changes.ask = true;
        }

        if (this.props.values.avg_spread !== nextProps.values.avg_spread) {
            changes.avg_spread = true;
        }
    }

    render() {
        const imgMapper = {
            'Bitcoin': 'https://s2.coinmarketcap.com/static/img/coins/16x16/1.png',
            'Ethereum': 'https://s2.coinmarketcap.com/static/img/coins/16x16/1027.png',
            'EOS': 'https://s2.coinmarketcap.com/static/img/coins/16x16/1765.png',
            'Litecoin': 'https://s2.coinmarketcap.com/static/img/coins/16x16/2.png',
            'Bitcoin Cash': 'https://s2.coinmarketcap.com/static/img/coins/16x16/1831.png',
        };

        return (
            <TableRow>
                <TableRowColumn><img src={imgMapper[this.props.coinName]}/> {this.props.coinName}</TableRowColumn>
                <TableRowColumn className={changes.bid ? 'flash-update-grey' : ''}>{this.props.values && this.props.values.bid}</TableRowColumn>
                <TableRowColumn className={changes.ask ? 'flash-update-grey' : ''}>{this.props.values && this.props.values.ask}</TableRowColumn>
                <TableRowColumn
                className={this.props.values.spread < this.props.values.avg_spread ? 'positive-green' : 'negative-red'}>
                    {this.props.values && this.props.values.spread}
                </TableRowColumn>
                <TableRowColumn className={changes.avg_spread ? 'flash-update-grey' : ''}>{this.props.values && this.props.values.avg_spread}</TableRowColumn>
            </TableRow>
        )
    }
}
