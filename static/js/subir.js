$(document).ready(function () {
  $("#file-container").click(function () {
      $("#file-input").click();
  });

  $("#file-input").change(function () {
      var fileName = $(this).val().split('\\').pop();
      $("#selected-file").text(fileName);
  });
});