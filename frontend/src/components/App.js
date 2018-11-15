import React, { Component } from 'react';
import { Router, Route, Redirect, Switch } from 'react-router';
import { connect } from 'react-redux';
import history from 'utils/history';

import Login from './Login';
import Home from './Home';
import Create from './Create';
import Detail from './Detail';

export class App extends Component {
  render() {
    let routes = [];
    if (!this.props.loggedIn) {
      routes = [
        <Route path="/" exact component={Login} key="login" />,
        <Redirect to="/" key="redirect_login" />,
      ];
    } else {
      routes = [
        <Route path="/home" component={Home} key="home" />,
        <Route path="/create" component={Create} key="create" />,
        <Route path="/detail/:eventId" component={Detail} key="detail" />,
        <Redirect to="/home" key="redirect_home" />,
      ];
    }

    return (
      <div className="App">
        <Router history={history}>
          <React.Fragment>
            <Switch>
              {routes}
            </Switch>
          </React.Fragment>
        </Router>
      </div>
    );
  }
}


const mapStateToProps = ({ user }) => ({
  loggedIn: user.loggedIn,
});

const mapDispatchToProps = {
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
