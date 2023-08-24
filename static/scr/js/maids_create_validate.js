odoo.define("ms_housemaid.my_maids_portal_new_form_view", function (require) {
  "use strict";

  var publicwidget = require("web.public.widget");
  publicwidget.registry.my_maids_portal_new_form_view =
    publicwidget.widget.extend({
      selector: "#new_maid_create_form",
      events: {
        'submit': "_onSubmit",
      },

      _onSubmi: function () {
        console.log(" Hi first odoo js");
        alert("hi");
      },
    });
});
