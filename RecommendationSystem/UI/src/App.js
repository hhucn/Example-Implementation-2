/*global chrome */
import React from 'react';
import './App.css';
import SelectTextButton from "./components/SelectTextButton";
import SuggestionList from "./components/SuggestionList";
import * as ReactDOM from "react-dom";
import NoSelectionHint from "./components/NoSelectionHint"
import Loading from "./components/Loading";
import NoSuggestions from "./components/NoSuggestions";
import ErrorScreen from "./components/ErrorScreen";
import CommentCarousel from "./components/CommentCarousel"


/**
 * App.js generates the UI of the plugin and renders different views depending on the response from the backend server.
 */



chrome.runtime.onMessage.addListener(
    function (request) {
        console.log("bar");
        if (request.message === "Sending_recommendations") {
            let results = request.recommendations;
            console.log(results)
            //ReactDOM.render(<SuggestionList
            //    suggestions={results}/>, document.getElementById('root'));
            ReactDOM.render(<CommentCarousel suggestions={results}/>, document.getElementById('root'));
        }
    }
)


/**
 * Renders start page of plugin.
 * @returns {JSX.Element}
 * @constructor
 */
function App() {
    return (
        <div className="App" id="App">
            <SelectTextButton/>
        </div>
    );
}

export default App;