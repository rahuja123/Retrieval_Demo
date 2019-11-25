$(document).on('click', '.img_style', function() {
  $(this).toggleClass('img_style_true')
});

$(document).on('click', '#show_results', function() {
  var x = document.getElementById("floormaps_output");
  var y= document.getElementById("experimental_section");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display= "block";
  } else {
    x.style.display = "none";
    y.style.display ="none";
  }
});



$(document).on('click', '#show_locations', function() {
    var annotation = [];
    $('.img_style_true').map(function() {
      annotation.push($(this).attr('id'));
    })
    var y= document.getElementById("experimental_section");
    if (y.style.display === "none") {
      y.style.display= "block";
    }

    console.log(annotation);
    $.ajax({
      url: '/',
      dataType: 'json',
      contentType: 'application/json',
      method: 'POST',
      data: JSON.stringify({
        'annotated': annotation,
        'finished': true,
      }),
      // success: function (msg) {
      //   if (msg.status='finished') {
      //     window.location.reload(false);
      //     // If we needed to pull the document from
      //     //  the web-server again (such as where the document contents
      //     //  change dynamically) we would pass the argument as 'true'.
      //   }
      // }
    });

  }
);

//
