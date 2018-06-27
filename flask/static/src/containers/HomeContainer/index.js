import React from 'react';
import openSocket from 'socket.io-client';

/* components */
import { Home } from '../../components/Home';



class HomeContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {liveData: {}};

        const socket = openSocket('http://ec2-54-156-187-154.compute-1.amazonaws.com:5000');
        socket.on('liveData', (data) => {
            console.log('received new data: ', data);
            this.setState({
              liveData: data
            });
        });
    }
    render() {
        return (
            <section>
                <Home liveData={this.state.liveData} />
            </section>
        );
    }
}

export const HomeContainer = HomeContainer
