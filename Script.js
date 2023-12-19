console.log("Script loaded!");

function showGitCode() {
    if (document.getElementById("gitCode1").style.display=="none"){
        document.getElementById("gitCode1").style.display="block"
    }
    else{
        document.getElementById("gitCode1").style.display="none"
    }
}

function hideGitCode() {
    if (document.getElementById("gitCode1").style.display=="block"){
        document.getElementById("gitCode1").style.display="none"
    }
}

let homeBodyText = document.getElementById("maintext")
let homeButtonClick = document.getElementById("button")

function changeTextHomepage() {
    document.getElementById("maintext").innerHTML = "hi"
    document.getElementById("maintext").style.display="block"
}


homeBodyText.addEventListener("mouseover", changeTextHomepage)
homeButtonClick.addEventListener("click", function (){
    homeBodyText.innerHTML="yo"
})

let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        myBtn.style.display = "block";
    } else {
        myBtn.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

var navbar = document.querySelector('.topnav');

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 100) {
        navbar.classList.add('hidden');
    } else {
        navbar.classList.remove('hidden');
    }
})

function showNoah() {
    if (document.getElementById("noahImage").style.display=="none"){
        document.getElementById("noahImage").style.display="block"
        document.getElementById('button').style.display="none"

    }
    else{
        document.getElementById("noahImage").style.display="none"
    }
}

/* Get the dropdown button and menu */
var dropdownBtn = document.getElementsByClassName("dropbtn");
var dropdownContent = document.getElementsByClassName("dropdown-content");

/* Loop through all dropdown buttons */
for (var i = 0; i < dropdownBtn.length; i++) {
    /* When the user clicks on the button, toggle between hiding and showing the dropdown content */
    dropdownBtn[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.parentElement.querySelector(".dropdown-content");
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function toggleDarkMode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
    console.log("Dark mode toggled");
}

window.addEventListener('scroll', function() {
    var footer = document.querySelector('footer');
    var main = document.querySelector('main');
    var footerHeight = footer.offsetHeight;
    var mainHeight = main.offsetHeight;
    var scrollPosition = window.scrollY || window.pageYOffset;

    // Adjust the footer position based on scroll position
    if (scrollPosition > mainHeight - window.innerHeight) {
        footer.style.position = 'fixed';
        footer.style.bottom = '0';
    } else {
        footer.style.position = 'relative';
        footer.style.bottom = 'auto';
    }
});

function scrollToTop() {
    window.scrollTo({top: 0,
        behavior: 'smooth'
    });

}