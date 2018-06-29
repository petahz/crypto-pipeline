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
        if (this.props.values.bid !== nextProps.values.bid) {
            changes.bid = true;
        }

        if (this.props.values.ask !== nextProps.values.ask) {
            changes.ask = true;
        }

        if (this.props.values.avg_spread !== nextProps.values.avg_spread) {
            changes.avg_spread = true;
        }

        changes = {
            bid: false,
            ask: false,
            avg_spread: false,
        };
    }

    shouldComponentUpdate(nextProps) {
        const differentBid = this.props.values.bid !== nextProps.values.bid;
        const differentAsk = this.props.values.ask !== nextProps.values.ask;
        return differentBid || differentAsk;
    }

    render() {
        return (
            <TableRow>
                <TableRowColumn>{this.props.coinName}</TableRowColumn>
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
