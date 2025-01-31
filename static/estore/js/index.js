// window.onscroll = ()=>{
//     if (window.scrollY > 50){
//         scroll = window.scrollY;
//         $("#header").addClass('hide');
//     }else if(window.scrollY > -50){
//         $("#header").removeClass('hide');
//     }
//     // if(document.body.scrollTop > 50 || document.documentElement.scrollTop > 50){
//     //     document.getElementById('header').style.top = "-4rem";
//     // }else if(document.body.scrollTop > -50 || document.documentElement.scrollTop > -50){
//     //     document.getElementById('header').style.top = "0";
//     // }else{
//     //     document.getElementById('header').style.top = "0";
//     // }
// }

// cancel button
const cancelBtn = ()=>{
    history.back();
}

// open  search bar
const openSearch = ()=>{
    closeMenu();
    document.getElementById('search-input').style.top = "4rem";
    document.getElementById('search-input').style.display = "block";
}

// close search bar
const closeSearch = ()=>{
    document.getElementById('search-input').style.top = "0";
    document.getElementById('search-input').style.display = "none";
    document.getElementById('suggestion').style.display = "none";
    document.getElementById('header-input').value ='';
}
// text suggest on input
const suggestText = ()=>{
    document.getElementById('suggestion').style.display = "block";
    console.log(document.getElementById('header-input').value);
}

// open menu 
const openMenu = ()=>{
    closeSearch();
    document.getElementById('menu-drawer').style.right = "0";
}
//close menu
const closeMenu = ()=>{
    document.getElementById('menu-drawer').style.right = "-70%";
}

// toggle parword view or hide 
const togglePassword = (eye)=>{
    if(eye){
        document.getElementById('password').type = 'text';
        document.getElementById('pass-eye').style.display = 'block';
    }else{
        document.getElementById('password').type = 'password';
        document.getElementById('pass-eye').style.display = 'none';
    }
}

// toggle password field for registration form
const toggleRegisterPassword = (eye)=>{
    if(eye){
        document.getElementById('reg-password').type = 'text';
        document.getElementById('reg-pass-eye').style.display = 'block';
    }else{
        document.getElementById('reg-password').type = 'password';
        document.getElementById('reg-pass-eye').style.display = 'none';
    }
}

// toggle confirm password field for registration form
const toggleRegisterConfirmPassword = (eye)=>{
    if(eye){
        document.getElementById('reg-conf-password').type = 'text';
        document.getElementById('conf-pass-eye').style.display = 'block';
    }else{
        document.getElementById('reg-conf-password').type = 'password';
        document.getElementById('conf-pass-eye').style.display = 'none';
    }
}

// checkout form add quantity 
function addQuantity(id, price){
    var quantity = document.getElementById(`product-${id}`);
    quantity.value = ++quantity.value;
    price = price * quantity.value;
    var amount = document.getElementById(`tot_price-${id}`);
    amount.value = Math.round((price + Number.EPSILON)*100)/100;
}
//  checkout form subtract quantity
function subQuantity(id, price){
    var quantity = document.getElementById(`product-${id}`);
    if(parseInt(quantity.value)>1){
        var amount = document.getElementById(`tot_price-${id}`);
        quantity.value = --quantity.value;
        price = price * quantity.value;
        amount.value = Math.round((price + Number.EPSILON)*100)/100;
    }
}

//Add to cart button
function addToCart(id, name, price){
    var cart = [];
    if(localStorage.getItem('Cart')==null){
        localStorage.setItem('Cart',JSON.stringify(cart));
    }else{
        var local = localStorage.getItem('Cart');
        cart = JSON.parse(local);
    }
    cart[cart.length] = ({product_id:id, product_name:name, quantity:1, price:price});
    console.log(cart);
    localStorage.setItem('Cart', JSON.stringify(cart));
}


// show product description
function showDesc(){
    document.getElementById('descShowBtn').style.display = 'none';
    document.getElementById('descHideBtn').style.display = 'block';
    const descPara = document.getElementById('description').style.height = '100%';
}
// Hide product description
function hideDesc(){
    document.getElementById('descShowBtn').style.display = 'inline';
    document.getElementById('descHideBtn').style.display = 'none';
    const descPara = document.getElementById('description').style.height = '8rem';
}