import React from 'react';
import { connect } from 'react-redux';

import { login, signup } from 'actions/user';

import history from 'utils/history';

export class Login extends React.Component {
  state = {
    email: '',
    username: '',
    password: '',
  }

  inputChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  login = () => {
    const { username, password } = this.state;
    this.props.login(username, password).then((response) => {
      if (response.result === 'error') return;
      history.push('/home');
    });
  }

  signup = () => {
    const { email, username, password } = this.state;
    this.props.signup(email, username, password).then((response) => {
      if (response.result === 'error') return;
      history.push('/home');
    });
  }

  render() {
    return (
      <React.Fragment>
        Email
        <input type="text" onChange={this.inputChange} name="email" />
        <br />
        Username
        <input type="text" onChange={this.inputChange} name="username" />
        <br />
        Password
        <input type="password" onChange={this.inputChange} name="password" />
        <br />
        <button type="button" onClick={this.login}>Login</button>
        <button type="button" onClick={this.signup}>Signup</button>
      </React.Fragment>
    );
  }
}

const mapStateToProps = null;

const mapDispatchToProps = { login, signup };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Login);
