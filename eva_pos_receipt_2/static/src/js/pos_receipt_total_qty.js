/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
// import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";
import { useContext, useState, onMounted } from "@odoo/owl";

// Extend the OrderReceipt component
// export class ExtendedOrderReceipt extends OrderReceipt {
//     get totalQuantity() {
//         return this.props.data.total_quantity || 0;
//     }
// }

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.receipt_state = useState({ total_quantity: 0 });
    },
    async validateOrder(isForceValidate) {
        // console.log("Validate order button clicked!");
        // const total_quantity = this.itemCount();
        // console.log("Total Quantity:", total_quantity);
        // Store total quantity in the state
        // this.receipt_state = total_quantity;
        // console.log(this.receipt_state, "STATE")
        await super.validateOrder(isForceValidate);
    },
    // itemCount() {
    //     const order = this.currentOrder;
    //     if (order) {
    //         const orderlines = order.get_orderlines();
    //         let total_quantity = 0;
    //         orderlines.forEach((line) => {
    //             total_quantity += line.get_quantity();
    //         });
    //         return total_quantity;
    //     }
    //     return 0;
    // },
});

import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
// odoo/auto/addons/point_of_sale/static/src/app/screens/receipt_screen/receipt/order_receipt.js
// import { patch } from "@web/core/utils/patch";
// import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(OrderReceipt.prototype, {
    setup() {
        super.setup();

        this.ui = useState(useService("ui"));
        this.totalQuantity = 0;
        // console.log(this.props);

        const orderlines = this.props.data.orderlines;
        // console.log(orderlines, "OL");

        // let totalQuantity = 0;
        orderlines.forEach((line) => {
            this.totalQuantity += line.qty;
        });
        // console.log(this.totalQuantity, "QTY");

        return this.totalQuantity

        // this.totalQuantity.setValue(totalQuantity);

        //     onMounted(async () => {
        //         console.log(this.props);

        //         const orderlines = this.props.data.orderlines;
        //         console.log(orderlines, "OL");

        //         let totalQuantity = 0;
        //         orderlines.forEach((line) => {
        //             totalQuantity += line.qty;
        //         });
        //         console.log(totalQuantity, "QTY");

        //         this.totalQuantity.setValue(totalQuantity);
        //     }
        // );
    },
});



