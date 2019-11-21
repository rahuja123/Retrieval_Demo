var button1 = document.getElementById('show_results'); // Assumes element with id='button'

button1.onclick = function() {
    var div = document.getElementById('floormaps_output');
    if (div.style.display !== 'none') {
        div.style.display = 'none';
    }
}


var button2 = document.getElementById('show_locations'); // Assumes element with id='button'

button2.onclick = function() {
    var div = document.getElementById('floormaps_output');
    if (div.style.display == 'none') {
        div.style.display = 'block';
    }
}
