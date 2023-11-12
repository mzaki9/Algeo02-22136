import React from "react";
import MultiImageUpload from "./multiImageUpload";
class DataSetBox extends React.Component{
    render(){
        return(
            <div className="uploadDataSetButton">
                <MultiImageUpload></MultiImageUpload>
            </div>
        );
    }
}
export default DataSetBox;