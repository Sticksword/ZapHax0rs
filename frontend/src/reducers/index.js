import { combineReducers } from 'redux';
import FilesReducer from './reducer_files';

const rootReducer = combineReducers({
  files: FilesReducer
});

export default rootReducer;
