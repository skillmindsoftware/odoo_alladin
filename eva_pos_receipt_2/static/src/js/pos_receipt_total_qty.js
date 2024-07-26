/** @odoo-module **/
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.receipt_state = useState({ total_quantity: 0 });
    },
    async validateOrder(isForceValidate) {
        await super.validateOrder(isForceValidate);
    },

});

patch(OrderReceipt.prototype, {
    setup() {
        super.setup();
        this.ui = useState(useService("ui"));
        this.totalQuantity = 0;
        console.log(this.props);

        const orderlines = this.props.data.orderlines;
        // console.log(orderlines, "OL");
        orderlines.forEach((line) => {
            this.totalQuantity += line.qty;
        });
        // console.log(this.totalQuantity, "QTY");

        return this.totalQuantity
    },
});



