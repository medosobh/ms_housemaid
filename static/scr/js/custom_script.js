odoo.define("attendance_regularization.custom_script", function (require) {
  "use strict";

  var core = require("web.core");
  var FieldDateTime = core.form_widget_registry.get("datetime-local");

  FieldDateTime.include({
    pickerDateTimeFormat: "YYYY-MM-DD",
  });
});
