var $messages = $(".messages-content");
var d;
var h;
var m;
var i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar("scrollTo", "bottom", {
    scrollInertia: 10,
    timeout: 0
  });
}

function insertMessage() {
  msg = $(".message-input").val();
  if ($.trim(msg) == "") {
    return false;
  }
  $('<div class="message message-personal">' 
    + msg + "</div>"
  ).appendTo($(".mCSB_container")).addClass("new");
  
  $(".message-input").val(null);
  
  updateScrollbar();
  
  $('<div class="message loading new">'+
    '<img class="avatar" src="./static/bot.png" /><span></span>'+
    '</div>'
  ).appendTo($(".mCSB_container"));
  
  updateScrollbar();
  
  $.get("/get", { msg: msg }).done(function(data) {
    $(".message.loading").remove();

    $('<div class="message new">'+
      '<img class="avatar" src="./static/bot.png" />' +
      data +
      '</div>'
    ).appendTo($(".mCSB_container")).addClass("new");
    updateScrollbar();
    i++;
  });
}

$(".message-submit").click(function() {
  insertMessage();
});

$(window).on("keydown", function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
});

var Fake = ["¡Hola! Soy IsaBot, en que te puedo ayudar?"];

function fakeMessage() {
  if ($(".message-input").val() != "") {
    return false;
  }
  $(
    '<div class="message loading new"><img class="avatar" src="./static/bot.png" /><span></span></div>'
  ).appendTo($(".mCSB_container"));
  updateScrollbar();

  setTimeout(function() {
    $(".message.loading").remove();
    $(
      '<div class="message new"><img class="avatar" src="./static/bot.png" />' +
        Fake[i] +
        "</div>"
    )
      .appendTo($(".mCSB_container"))
      .addClass("new");
    updateScrollbar();
    i++;
  }, 1000);
}

$(".button").click(function() {
  $(".menu .items span").toggleClass("active");
  $(".menu .button").toggleClass("active");
});

