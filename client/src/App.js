import React, {Component} from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages';
import US from './pages/US';
import World from './pages/World';

class App extends Component {
  render() {
    return (
      <Router>
         <Navbar></Navbar>
         <Switch>
           <Route path="/" exact component={Home}></Route>
           <Route path="/US" component={US}></Route>
           <Route path="/World" component={World}></Route>
         </Switch>
      </Router>
    );
  }
}
export default App;


