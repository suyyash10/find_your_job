var skew = document.querySelector(".hum")
skew.addEventListener("click",()=>{
    document.body.classList.toggle("skew-open");
});

var about = document.querySelector(".scroll-about",".scroll-about2")
about.addEventListener("click",()=>{
    window.scrollTo({
        top: 545,
        behavior: 'smooth',
    });
});

var home = document.querySelector(".scroll-home")
home.addEventListener("click",()=>{
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    });
});

var contact = document.querySelector(".scroll-contact")
contact.addEventListener("click",()=>{
    window.scrollTo({
        top: 100000,
        behavior: 'smooth',
    });
});

window.addEventListener("scroll", () => { 
    document.body.classList.add("showit");
  });

