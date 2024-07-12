/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        console.log("Setup ProductScreen for disabling %disc and Price buttons");
    },

    getNumpadButtons() {
        const buttons = super.getNumpadButtons();
        return buttons.map(button => {
            if (button.command === 'discount' || button.command === 'price') {
                return { ...button, disabled: true };
            }
            return button;
        });
    },

    // Remove unnecessary methods
    // onNumpadClick and updateSelectedOrderline are not needed for this modification
});