import React from 'react';
import { connect } from 'react-redux';
import { uploadFile, uploadDemo } from '../actions/uploadActions';

class FileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.submitForm = this.submitForm.bind(this);
    this.submitDemo = this.submitDemo.bind(this);
    this.handleDemoChange = this.handleDemoChange.bind(this);
  }

  handleDemoChange(event) {
    this.setState({value: event.target.value});
  }

  submitDemo(e) {
    e.preventDefault();
    let data = new FormData();
    data.append('demo', this.state.value);
    console.log(this.state.value);
    this.props.uploadDemo(data);

  }

  submitForm(e) {
    e.preventDefault();
    console.log('hello from submitForm');
    let data = new FormData();
    data.append('foo', 'bar');
    data.append('file', this.fileUpload.files[0]);
    console.log(data);
    this.props.uploadFile(data);

  }

  render() {
    return (
      <div>
        <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
        <form encType='multipart/form-data' onSubmit={this.submitForm}>
          <input ref={(input) => { this.fileUpload = input; }} type='file' name='file' />
          <input type='submit' value='UploadFile' />
        </form>
        <form onSubmit={this.submitDemo}>
          <input type='text' value={this.state.value} onChange={this.handleDemoChange} />
          <input type='submit' value='UploadDemo' />
        </form>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => {
  return {
    uploads: state
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    uploadFile: file => dispatch(uploadFile(file)),
    uploadDemo: demo => dispatch(uploadDemo(demo))
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FileUpload);
