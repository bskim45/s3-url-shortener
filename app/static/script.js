function addMessage(text) {
  $('#message').html(text).show()
}

function shortenLink(apiUrl, longUrl, alias) {
  $.ajax(apiUrl, {
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({url: longUrl, alias: alias})
  }).done(function (responseJSON) {
    const link = $("<a>");
    link.attr("href", responseJSON.data.url);
    link.text(responseJSON.data.url);
    addMessage(link)
  }).fail(function (data) {
    addMessage(data.responseJSON.msg);
  })
}

$(document).ready(function () {
  $('form').submit(function (event) {
    event.preventDefault();
    addMessage('...');
    shortenLink(event.target.action, event.target.url.value, event.target.alias.value)
  })
});
