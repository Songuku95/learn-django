import React from 'react';
import { connect } from 'react-redux';
import DatePicker from 'react-datepicker';
import moment from 'moment';

import { createEvent } from 'actions/event';
import { uploadImage } from 'actions/user';

import { API_ENDPOINT } from 'constants/common';

import history from 'utils/history';
import { formatDate } from 'utils/time';

import Header from '../Header';

const ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg'];
const MAX_SIZE = 4 * 1024 * 1024;

export class Create extends React.Component {
  state = {
    imagePaths: [],
    tags: '',
    title: '',
    description: '',
    address: '',
    latitude: 0,
    longitude: 0,
    startDate: moment(),
    endDate: moment(),
    file: null,
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

  fileChange = (e) => {
    const file = e.target.files[0];
    if (file === undefined) {
      this.setFile(e, null);
      return;
    }
    if (file.size > MAX_SIZE) {
      alert('File too large');
      this.setFile(e, null);
      return;
    }
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (ALLOWED_EXTENSIONS.indexOf(fileExtension) === -1 || fileExtension === file.name.toLowerCase()) {
      alert('Only .jpg, .jpeg, .png files are allowed');
      this.setFile(e, null);
      return;
    }
    this.setFile(e, file);
  }

  setFile = (e, file) => {
    this.setState({ file });
    if (file === null) e.target.value = null;
  }

  addImage = () => {
    const file = this.state.file;
    if (file === null) return;
    this.props.uploadImage(file).then((response) => {
      if (response.result === 'error') return;
      this.setState({
        imagePaths: [...this.state.imagePaths, response.reply.imagePath],
      });
    });
  }

  deleteImage = (index) => {
    const imagePaths = [...this.state.imagePaths];
    imagePaths.splice(index, 1);
    this.setState({
      imagePaths,
    });
  }

  submit = () => {
    const request = {
      ...this.state,
      tags: this.state.tags.split(','),
      startDate: formatDate(this.state.startDate.unix()),
      endDate: formatDate(this.state.endDate.unix()),
      latitude: parseFloat(this.state.latitude),
      longitude: parseFloat(this.state.longitude),
    };
    this.props.createEvent(request).then((response) => {
      if (response.result === 'error') return;
      history.push(`/detail/${response.reply.id}`);
    });
  }

  gotoHomePage = () => {
    history.push('/home');
  }

  render() {
    return (
      <React.Fragment>
        <Header />

        <button type="button" onClick={this.gotoHomePage}>Back</button>
        <br />
        <br />


        <b>Title: </b>
        <input type="text" name="title" onChange={this.inputChange} value={this.state.title} />
        <br />

        <b>Description: </b>
        <input type="text" name="description" onChange={this.inputChange} value={this.state.description} />
        <br />

        <b>Start date: </b>
        <DatePicker
          selected={this.state.startDate}
          onChange={date => this.dateChange(date, 'startDate')}
        />
        <br />

        <b>End date: </b>
        <DatePicker
          selected={this.state.endDate}
          onChange={date => this.dateChange(date, 'endDate')}
        />
        <br />

        <b>Address: </b>
        <input type="text" name="address" onChange={this.inputChange} value={this.state.address} />
        <br />

        <b>Latitude: </b>
        <input type="text" name="latitude" onChange={this.inputChange} value={this.state.latitude} />
        <br />

        <b>Longitude: </b>
        <input type="text" name="longitude" onChange={this.inputChange} value={this.state.longitude} />
        <br />

        <b>Tags: </b>
        <input type="text" name="tags" onChange={this.inputChange} value={this.state.tags} />
        <br />

        <br />
        {
          this.state.imagePaths.map((path, index) => (
            <React.Fragment key={path}>
              <img src={API_ENDPOINT + path} key={path} alt="" />
              <button type="button" onClick={() => this.deleteImage(index)}> Delete </button>
              <br />
            </React.Fragment>
          ))
        }
        <br />

        <br />
        <input
          type="file"
          onChange={this.fileChange}
          accept={ALLOWED_EXTENSIONS.map(element => `.${element}`).join(', ')}
        />
        <button type="button" onClick={this.addImage}>Add image</button>

        <br />
        <br />
        <br />
        <button type="button" onClick={this.submit}>Submit</button>
      </React.Fragment>
    );
  }
}

const mapStateToProps = null;

const mapDispatchToProps = { createEvent, uploadImage };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Create);
