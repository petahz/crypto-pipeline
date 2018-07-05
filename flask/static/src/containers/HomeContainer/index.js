import React from 'react';
import openSocket from 'socket.io-client';

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
    render() {
        return (
            <section>
                <DropDownMenu value={this.state.value} onChange={this.handleChange}>
                  <MenuItem value={'kraken'} primaryText="Kraken" />
                </DropDownMenu>
                <DropDownMenu value={this.state.value} onChange={this.handleChange}>
                  <MenuItem value={'USD'} primaryText="USD" />
                </DropDownMenu>
                <Home liveData={this.state.liveData} />
            </section>
        );
    }
}
