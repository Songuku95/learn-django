import React from 'react';
import { connect } from 'react-redux';

import { searchEvent, getEventList } from 'actions/event';

import Header from 'components/Header';

import history from 'utils/history';

export class Home extends React.Component {
  componentDidMount() {
    this.props.searchEvent().then((response) => {
      console.log(response);
      if (response.result === 'error') return;
      this.props.getEventList(response.reply.ids.slice(0, 10));
    });
  }

  gotoCreatePage = () => {
    history.push('/create');
  }

  gotoPageDetail = (id) => {
    history.push(`/detail/${id}`);
  }

  render() {
    return (
      <React.Fragment>
        <Header />
        <button type="button" onClick={this.gotoCreatePage}>Create new event</button>
        <br />
        <br />
        <table style={{ width: '100%', textAlign: 'center' }}>
          <thead>
            <tr>
              <th>id</th>
              <th>Title</th>
              <th>Address</th>
            </tr>
          </thead>
          {
            this.props.list.map(e => (
              <tbody key={e.id}>
                <tr onClick={() => this.gotoPageDetail(e.id)} style={{ cursor: 'pointer' }}>
                  <td>{e.id}</td>
                  <td>{e.title}</td>
                  <td>{e.address}</td>
                </tr>
              </tbody>
            ))
          }

        </table>

      </React.Fragment>
    );
  }
}

const mapStateToProps = ({ event }) => ({
  ids: event.ids,
  list: event.list,
});

const mapDispatchToProps = { searchEvent, getEventList };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Home);
