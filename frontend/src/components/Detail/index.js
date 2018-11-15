import React from 'react';
import { connect } from 'react-redux';
import moment from 'moment';

import { getEventDetail } from 'actions/event';

import history from 'utils/history';

import { API_ENDPOINT } from 'constants/common';
import Header from '../Header';


export class Detail extends React.Component {
  componentDidMount() {
    const eventId = parseInt(this.props.match.params.eventId);
    this.props.getEventDetail(eventId);
  }

  gotoHomePage = () => {
    history.push('/home');
  }

  render() {
    const event = this.props.event;
    return (
      <React.Fragment>
        <Header />

        <button type="button" onClick={this.gotoHomePage}>Back</button>
        <br />
        <br />

        <b>ID: </b>
        {event.id}
        <br />


        <b>Title: </b>
        {event.title}
        <br />

        <b>Description: </b>
        {event.description}
        <br />

        <b>Start date: </b>
        {moment.unix(event.startDate).format('MMM DD YYYY')}
        <br />

        <b>End date: </b>
        {moment.unix(event.endDate).format('MMM DD YYYY')}
        <br />

        <b>Address: </b>
        {event.address}
        <br />

        <b>Latitude: </b>
        {event.latitude}
        <br />

        <b>Longitude: </b>
        {event.longitude}
        <br />

        <b>Tags: </b>
        {event.tags.join(', ')}
        <br />

        <br />
        {
          event.images.map(e => (
            <img src={API_ENDPOINT + e.path} key={e.path} alt="" />
          ))
        }
        <br />

      </React.Fragment>
    );
  }
}

const mapStateToProps = ({ event }) => ({
  event: event.current,
});

const mapDispatchToProps = { getEventDetail };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Detail);
