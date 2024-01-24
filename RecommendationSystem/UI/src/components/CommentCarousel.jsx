import React from 'react';
import ReactDOM from 'react-dom';

import { Swiper, SwiperSlide } from "swiper/react";

// Import Swiper styles
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

import "./styles.css";

// import required modules
import { Navigation, Pagination, Mousewheel, Keyboard } from "swiper";

function slideElement(comment){
    return (<SwiperSlide><div id="slide-element-comment">{comment[0]}</div></SwiperSlide>);
}

function renderSlides(comments){
        return comments.map((comment) => slideElement(comment));
}

function CommentCarousel(props) {
    return (
    <div id="comment-carousel">
    <Swiper
        cssMode={true}
        navigation={true}
        pagination={true}
        mousewheel={true}
        keyboard={true}
        modules={[Navigation, Pagination, Mousewheel, Keyboard]}
        className="mySwiper"
      >
        {renderSlides(props.suggestions)}
      </Swiper>
      </div>
  );
}

export default CommentCarousel;