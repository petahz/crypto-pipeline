import React from 'react';

import {blueGrey100, blueGrey500, grey700} from 'material-ui/styles/colors';
import lightBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

/* application components */
import { Header } from '../../components/Header';

/* global styles for app */
import './styles/app.scss';

const muiTheme = getMuiTheme(lightBaseTheme, {
    palette: {
        accent1Color: blueGrey100,
        accent3Color: blueGrey100,
        alternateTextColor: '#fff',
        canvasColor: grey700,
        primary1Color: blueGrey500,
    }
});

class App extends React.Component { // eslint-disable-line react/prefer-stateless-function
    static propTypes = {
        children: React.PropTypes.node,
    };

    render() {
        return (
            <MuiThemeProvider muiTheme={muiTheme}>
                <section>
                    <Header />
                    <div
                      className="container"
                      style={{ marginTop: 10, paddingBottom: 250 }}
                    >
                        {this.props.children}
                    </div>
                </section>
            </MuiThemeProvider>
        );
    }
}

export { App };
