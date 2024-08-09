/** @odoo-module **/
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

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
        this.totalQuantity = this.calculateTotalQuantity();
    },

    calculateTotalQuantity() {
        const orderlines = this.props.data.orderlines || [];
        console.log('Orderlines:', orderlines);

        let total = 0;
        orderlines.forEach((line) => {
            const qty = parseFloat(line.qty) || 0;
            console.log(`Product: ${line.product_name}, Quantity: ${qty}`);
            total += qty;
        });

        console.log('Total Quantity:', total);
        return total;
    },
});