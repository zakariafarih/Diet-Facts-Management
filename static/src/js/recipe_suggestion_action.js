odoo.define('diet_facts_management.recipe_suggestion_action', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');

    function openRecipeSuggestionWizard(product_id) {
        ajax.jsonRpc("/recipe_suggestion/get", 'call', {product_id: product_id})
            .then(function (data) {
                if (data.wizard_id) {
                    Dialog.alert(null, "Recipe Suggestion Wizard Opened (ID: " + data.wizard_id + ")");
                } else {
                    Dialog.alert(null, "No recipe suggestions available.");
                }
            })
            .catch(function (err) {
                Dialog.alert(null, "Error fetching recipe suggestions.");
            });
    }

    return {
        openRecipeSuggestionWizard: openRecipeSuggestionWizard
    };
});
