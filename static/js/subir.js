$(document).ready(function () {
  $("#file-container").click(function () {
      $("#file-input").click();
  });

  $("#file-input").change(function () {
      var fileName = $(this).val().split('\\').pop();
      $("#selected-file").text(fileName);
  });

  $("#file-container2").click(function () {
    $("#file-input2").click();
});

$("#file-input2").change(function () {
  var fileName = $(this).val().split('\\').pop();
  $("#selected-file2").text(fileName);
});
$("#file-container3").click(function () {
  $("#file-input3").click();
});

$("#file-input3").change(function () {
var fileName = $(this).val().split('\\').pop();
$("#selected-file3").text(fileName);
});

$("#file-container4").click(function () {
  $("#file-input4").click();
});

$("#file-input4").change(function () {
var fileName = $(this).val().split('\\').pop();
$("#selected-file4").text(fileName);
});

$("#file-container5").click(function () {
  $("#file-input5").click();
});

$("#file-input5").change(function () {
var fileName = $(this).val().split('\\').pop();
$("#selected-file5").text(fileName);
});
});