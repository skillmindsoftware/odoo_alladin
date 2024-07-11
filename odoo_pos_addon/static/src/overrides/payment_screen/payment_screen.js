/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.confirmation_code = "";
    },

    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.confirmation_code = json.confirmation_code || "";
    },

    set_confirmation_code(code) {
        this.confirmation_code = code;
    },

    get_confirmation_code() {
        return this.confirmation_code;
    },

    export_as_JSON() {
        const json = super.export_as_JSON();
        json.confirmation_code = this.confirmation_code;
        return json;
    },

    export_for_printing() {
        const result = super.export_for_printing();
        result.confirmation_code = this.confirmation_code;
        return result;
    },
});

patch(Order.prototype, {
    export_as_JSON() {
        const json = super.export_as_JSON();
        json.confirmation_code = this.get_confirmation_code();
        console.log("Exporting order JSON with confirmation code:", json.confirmation_code);
        return json;
    },

    get_confirmation_code() {
        const paymentLines = this.get_paymentlines();
        for (const line of paymentLines) {
            const code = line.get_confirmation_code();
            if (code) {
                return code;
            }
        }
        return null;
    },
});

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
    },

    async validateOrder(isForceValidate) {
        if (!await this.checkPaymentMethods()) {
            return;
        }
        this.logPaymentDetails();
        await this.sendConfirmationCodeToBackend();
        return super.validateOrder(isForceValidate);
    },

    logPaymentDetails() {
        const paymentLines = this.currentOrder.get_paymentlines();
        console.log("Payment Details:");
        paymentLines.forEach(line => {
            console.log(`Payment Method: ${line.payment_method.name}, Amount: ${line.amount}, Confirmation Code: ${line.get_confirmation_code()}`);
        });
    },

    async checkPaymentMethods() {
        const order = this.pos.get_order();
        const paymentLines = order.get_paymentlines();
        for (const line of paymentLines) {
            if (!this.isExemptPaymentMethod(line.payment_method) && !line.get_confirmation_code()) {
                const isConfirmed = await this.requestConfirmationCode(line);
                if (!isConfirmed) {
                    return false;
                }
            }
        }
        return true;
    },

    isExemptPaymentMethod(paymentMethod) {
        return paymentMethod.type === 'cash';
    },

    async requestConfirmationCode(paymentLine) {
        const { confirmed, payload: confirmationCode } = await this.popup.add(TextInputPopup, {
            title: _t("Payment Confirmation"),
            body: _t("Enter the payment confirmation code for ") + paymentLine.payment_method.name,
            placeholder: _t("Confirmation Code"),
        });

        if (confirmed) {
            if (confirmationCode === "") {
                await this.popup.add(ErrorPopup, {
                    title: _t("Invalid Confirmation"),
                    body: _t("A valid confirmation code is required to proceed with the payment."),
                });
                return false;
            }

            paymentLine.set_confirmation_code(confirmationCode);
            return true;
        } else {
            await this.popup.add(ErrorPopup, {
                title: _t("Confirmation Cancelled"),
                body: _t("Payment confirmation was cancelled."),
            });
            return false;
        }
    },

    async sendConfirmationCodeToBackend() {
        const order = this.currentOrder;
        const confirmationCode = order.get_confirmation_code();
        console.log("Attempting to send confirmation code:", confirmationCode);
        console.log("Order name:", order.name);
        if (confirmationCode) {
            try {
                const companyId = this.pos.config.company_id[0];
                console.log("Company ID:", companyId);
                const result = await this.orm.call(
                    'pos.order',
                    'update_order_confirmation_code',
                    [order.name, confirmationCode],
                    { context: { company_id: companyId } }
                );
                console.log("Backend call result:", result);
            } catch (error) {
                console.error("Error sending confirmation code to backend:", error);
                await this.showErrorPopup('Backend Error', 'Failed to send confirmation code to the server. Please try again or contact support.');
            }
        } else {
            console.log("No confirmation code to send");
        }
    },

    async showErrorPopup(title, body) {
        await this.showPopup('ErrorPopup', {
            title: this.env._t(title),
            body: this.env._t(body),
        });
    },
});