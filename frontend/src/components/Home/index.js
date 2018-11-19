import React from 'react';
import { connect } from 'react-redux';
import DatePicker from 'react-datepicker';
import moment from 'moment';

import { searchEvent, getEventList } from 'actions/event';

import history from 'utils/history';
import { formatDate } from 'utils/time';
import Header from '../Header';
import Pagination from './Pagination';

const ITEM_PER_PAGE = 20;

export class Home extends React.Component {
  state = {
    startDate: null,
    endDate: null,
    tag: '',
    page: 1,
  }

  componentDidMount() {
    this.search();
  }

  search = () => {
    const { startDate, endDate, tag } = this.state;
    const request = {};
    if (startDate) request.startDate = formatDate(startDate.unix());
    if (endDate) request.endDate = formatDate(endDate.unix());
    if (tag) request.tag = tag;

    this.props.searchEvent(request).then((response) => {
      if (response.result === 'error') return;
      this.setState({ page: 1 });
      this.props.getEventList(response.reply.ids.slice(0, ITEM_PER_PAGE));
    });
  }

  getPage = (page) => {
    this.setState({ page });
    this.props.getEventList(this.props.ids.slice((page - 1) * ITEM_PER_PAGE, page * ITEM_PER_PAGE));
  }

  inputChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  dateChange = (date, name) => {
    this.setState({
      [name]: date,
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
        <b>Start date: </b>
        <DatePicker
          selected={this.state.startDate}
          onChange={date => this.dateChange(date, 'startDate')}
        />

        <b>End date: </b>
        <DatePicker
          selected={this.state.endDate}
          onChange={date => this.dateChange(date, 'endDate')}
        />

        <b>Tag: </b>
        <input type="text" name="tag" onChange={this.inputChange} value={this.state.tag} />

        <button type="button" onClick={this.search}>Search</button>

        <br />
        <br />
        <br />
        <table style={{ width: '100%', textAlign: 'center' }}>
          <thead>
            <tr>
              <th>id</th>
              <th>Title</th>
              <th>Address</th>
              <th>Start date</th>
              <th>End date</th>
            </tr>
          </thead>
          {
            this.props.list.map(e => (
              <tbody key={e.id}>
                <tr onClick={() => this.gotoPageDetail(e.id)} style={{ cursor: 'pointer' }}>
                  <td><a href={`/detail/${e.id}`}>{e.id}</a></td>
                  <td><a href={`/detail/${e.id}`}>{e.title}</a></td>
                  <td>{e.address}</td>
                  <td>{moment.unix(e.startDate).format('MMM DD YYYY')}</td>
                  <td>{moment.unix(e.endDate).format('MMM DD YYYY')}</td>
                </tr>
              </tbody>
            ))
          }
        </table>


        <Pagination
          currentPage={this.state.page}
          totalItems={this.props.ids.length}
          itemsPerPage={ITEM_PER_PAGE}
          onPageChange={this.getPage}
        />

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
