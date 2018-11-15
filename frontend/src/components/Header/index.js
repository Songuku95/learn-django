import React from 'react';
import { connect } from 'react-redux';

import { getProfile, logout } from 'actions/user';

import history from 'utils/history';

export class Header extends React.Component {
  componentDidMount() {
    this.props.getProfile();
  }

  logout = () => {
    history.push('/');

    this.props.logout();
  }

  render() {
    return (
      <React.Fragment>
        Hello,
        {' '}
        {this.props.user.username}
        {' '}
        <button type="button" onClick={this.logout}>Logout</button>
        <br />
        <br />
      </React.Fragment>
    );
  }
}

const mapStateToProps = ({ user }) => ({
  user,
});

const mapDispatchToProps = { getProfile, logout };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Header);
