doo.define("ms_housemaid.my_maids_portal_new_form_view", function (require) {
  "use strict";

  var publicwidget = required(web.public.widget);
  publicwidget.registry.my_maids_portal_new_form_view =
    publicwidget.widget.exclude({
      selector: "",
      events: {
        submit: "_onSubmitButton",
      },

      _onSubmitButton: function (evt) {
        console.log(" Hi first odoo js");
      },
    });
});
