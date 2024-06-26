const $slider = $('.slide');
const $btnPrev = $('#prev-button');
const $btnNext = $('#next-button');

let currentSlide = 0;
let counterValue = 1;

$slider.eq(currentSlide).addClass('on');
$('#iterations').text('Iteração ' + counterValue + ' / ' + $slider.length)

function hideSlider() {
    $slider.removeClass('on');
}

function showSlider() {
    $slider.eq(currentSlide).addClass('on');
}

function nextSlider() {
    hideSlider();

    if (currentSlide === $slider.length - 1) {
        currentSlide = 0;
    } else {
        currentSlide++;
    }
    showSlider();
}

function prevSlider() {
    hideSlider();
    if (currentSlide === 0) {
        currentSlide = $slider.length - 1;
    } else {
        currentSlide--;
    }
    showSlider();
}

function updateCounterLabel() {
    $('#iterations').text('Iteração ' + counterValue + ' / ' + $slider.length)
}

function increaseValue() {
    if (counterValue == $slider.length) {
        counterValue = 1;
    } else {
        counterValue++;
    }
    updateCounterLabel();
}

function decreaseValue() {
    if (counterValue == 1) {
        counterValue = $slider.length;
        
    }
    else{
        counterValue--;
    }
    updateCounterLabel();
}

$btnNext.on('click', nextSlider);
$btnPrev.on('click', prevSlider);