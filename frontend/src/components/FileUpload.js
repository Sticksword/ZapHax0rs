import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import { connect } from 'react-redux';
import { uploadFile, uploadDemo } from '../actions/uploadActions';
import DataPiece from './DataPiece';

class FileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.submitFile = this.submitFile.bind(this);
    this.submitDemo = this.submitDemo.bind(this);
  }

  submitDemo() {
    let data = new FormData();
    data.append('demo', this.demoUpload.input.value);
    this.props.uploadDemo(data);

  }

  submitFile() {
    let data = new FormData();
    data.append('file', this.fileUpload.files[0]);
    this.props.uploadFile(data);

  }

  render() {
    return (
      <div>
        <h3>File Demo (csv, tsv, csvz, tsvz only)</h3>
        <input ref={(input) => { this.fileUpload = input; }} type='file' name='file' />
        <FlatButton label="Upload File" onClick={this.submitFile} />

        <h3>Single Phrase Demo</h3>
        <TextField name='demo' ref={(input) => { this.demoUpload = input; }} />
        <FlatButton label="Upload Demo" onClick={this.submitDemo} />


        {this.props.uploads.files.map((item) => <DataPiece key={item.id} item={item} /> )}

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
