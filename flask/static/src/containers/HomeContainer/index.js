import React from 'react';
import openSocket from 'socket.io-client';

/* components */
import { Home } from '../../components/Home';

const socket = openSocket('http://localhost:5000');
socket.on('liveData', (data) => {
    console.log('received new data: ', data);
});

export const HomeContainer = () =>
    <section>
        <Home />
    </section>;