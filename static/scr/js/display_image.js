odoo.define("ms_housemaid.my_maids_portal_new_form_view", function (require) {
  "use strict";

  const uploadPictureButton = document.querySelector(".photo-upload");

  uploadPictureButton.addEventListener("change", function () {
    displayPicture(this);
  });

  function displayPicture(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        document
          .getElementById("the-picture")
          .setAttribute("src", e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
    }
  }
});
