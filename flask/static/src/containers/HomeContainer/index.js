import React from 'react';
import openSocket from 'socket.io-client';

import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';

/* components */
import { Home } from '../../components/Home';


console.log('open socket');
const socket = openSocket('http://ec2-54-156-187-154.compute-1.amazonaws.com:5000');

export class HomeContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {liveData: {}, exchange: 'kraken', source_currency: 'USD'};

        socket.emit('next', {success: true});
        socket.on('liveData', (data) => {
            this.setState({
              liveData: data
            });
            socket.emit('next', {success: true});
        });
    }

    handleChange = (event, index, value) => this.setState({value});

    render() {
        return (
            <section>
                <DropDownMenu value={this.state.exchange} onChange={this.handleChange}>
                  <MenuItem value={'kraken'} primaryText="Kraken" />
                </DropDownMenu>
                <DropDownMenu value={this.state.source_currency} onChange={this.handleChange}>
                  <MenuItem value={'USD'} primaryText="USD" />
                </DropDownMenu>
                <Home liveData={this.state.liveData} />
            </section>
        );
    }
}
