import React from 'react';
import FileUpload from './FileUpload';
import AppBar from 'material-ui/AppBar';

class App extends React.Component {
  render () {
    return (
      <div>
        <AppBar title = "Xavier" />
        <FileUpload />
      </div>
    );
  }
}

export default App;
