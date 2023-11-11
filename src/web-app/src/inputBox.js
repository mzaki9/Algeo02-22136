import React from "react";
import ImageUpload from "./ImageUpload";
class InputBox extends React.Component{
    render() {
        return(
            <div className="boxInputImage">
                <div className="uploadImageButton">
                    <ImageUpload></ImageUpload>
                </div>
            </div>
        );
    }
}
export default InputBox;