//------------------------------------- OCR Script







//---------------------------------------------------------------- Banner Slider

        const slider = document.querySelector('.slider');
        const sliderItems = document.querySelectorAll('.slide');
        const prevButton = document.querySelector('.prev');
        const nextButton = document.querySelector('.next');
        let currentIndex = 0;

        setInterval(() => {
            currentIndex++;
            if (currentIndex > sliderItems.length - 1) {
                currentIndex = 0
            }
            updateSlider();
        },3000)

        prevButton.addEventListener('click', () => {
            currentIndex--;
            if (currentIndex < 0) {
                currentIndex = sliderItems.length - 1
            }
            updateSlider();
        });

        nextButton.addEventListener('click', () => {
            currentIndex++;
            if (currentIndex > sliderItems.length - 1) {
                currentIndex = 0
            }
            updateSlider();
            
        });
        
        function updateSlider () {
            console.log(currentIndex);
            slider.style.marginLeft = `-${currentIndex * 100}%`
        }





//---------------------------------------------------- Accordian 

        var accordian_heads = document.querySelectorAll('.head')

        accordian_heads.forEach((ele, index) => {
            ele.addEventListener('click', function(){
                var parent = this.parentElement
                var icon = this.querySelector('i')
                if(parent.classList.contains('open_accordian')){
                    parent.classList.remove('open_accordian')
                    icon.classList.add("fa-plus")
                    icon.classList.remove("fa-minus")
                }
                else{
                    removeAccordians()
                    parent.classList.add('open_accordian')
                    icon.classList.remove("fa-plus")
                    icon.classList.add("fa-minus")
                }
            })
        })
        function removeAccordians() {
            accordian_heads.forEach((ele, index) => {
                    var parent = ele.parentElement
                    var icon = ele.querySelector('i')
                    parent.classList.remove('open_accordian')
                    icon.classList.add("fa-plus")
                    icon.classList.remove("fa-minus")
            })
        }




//--------------------------------------------- testimonials Slider



const test_slider = document.querySelector('.test_slider');
const test_sliderItems = document.querySelectorAll('.test-slide');
const test_prevButton = document.querySelector('.test-prev');
const test_nextButton = document.querySelector('.test-next');
let count = 0;

setInterval(() => {
    count++;
    if (count > test_sliderItems.length - 1) {
        count = 0
    }
    updateTestimonial();
},3000)

test_prevButton.addEventListener('click', () => {
    count--;
    if (count < 0) {
        count = test_sliderItems.length - 1
    }
    updateTestimonial();
});

test_nextButton.addEventListener('click', () => {
    count++;
    if (count > test_sliderItems.length - 1) {
        count = 0
    }
    updateTestimonial();
});

function updateTestimonial () {
    console.log(count);
    test_slider.style.marginLeft = `-${count * 100}%`
}



// ----------------------------- Toogle Navbar 

var bars_btn = document.querySelector('.toggler')
var toggle_bar = document.querySelector('.toggle_bar')

bars_btn.addEventListener('click', function(){
    if(toggle_bar.classList.contains('h-0')){
        toggle_bar.classList.remove('h-0')
        toggle_bar.classList.add('h-[210px]')
    }
    else{
        toggle_bar.classList.remove('h-[210px]')
        toggle_bar.classList.add('h-0')
    }
});



// -------------------------------- scroll Events


var top_toggler = document.querySelector('.top-toggler');
var navbar = document.querySelector('.navbar');


window.addEventListener('scroll', function(){
    console.log(scrollY);
    if(scrollY > 400){
        navbar.classList.add('fixed_nav')
    }
    else{
        navbar.classList.remove('fixed_nav')
    }
    if(scrollY > 600){
        top_toggler.style.right = '0px'
    }
    else{
        top_toggler.style.right = '-60px'
    }
})