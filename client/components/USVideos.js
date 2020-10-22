import React, {Component} from 'react';

class USVideos extends Component {
  constructor(props) {
    super(props);
    this.state = {
      us_videos = []
    }
  }

  callAPI() {
      fetch("http://localhost:9000/testAPI")
          .then(res => res.json())
          .then(res => this.setState({ us_videos: res }));
  }

  componentWillMount() {
      this.callAPI();
  }

  render() {
    return (
      <div>
        <h2>Press this button to send some dumb data</h2>
        <button type="button" class="btn btn-primary">Primary</button>
        <ul>
          {this.state.us_videos.map(video =>
            <li>{video}</li>
          )}
        </ul>
      </div>
    );
  }
}
export default USVideos;


