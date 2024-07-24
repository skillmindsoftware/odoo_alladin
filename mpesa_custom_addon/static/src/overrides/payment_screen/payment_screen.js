/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
const { Component, onWillStart, onMounted, useRef, useState } = owl
import { loadJS, loadCSS } from "@web/core/assets"

patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.confirmation_code = "";
        this.mpesa_transaction_id = "";
    },

    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.confirmation_code = json.confirmation_code || "";
        this.mpesa_transaction_id = json.mpesa_transaction_id || "";
    },

    export_as_JSON() {
        const json = super.export_as_JSON();
        json.confirmation_code = this.confirmation_code;
        json.mpesa_transaction_id = this.mpesa_transaction_id;
        return json;
    },

    export_for_printing() {
        const result = super.export_for_printing();
        result.confirmation_code = this.confirmation_code;
        result.mpesa_transaction_id = this.mpesa_transaction_id;
        return result;
    },
});

patch(Order.prototype, {
    export_as_JSON() {
        const json = super.export_as_JSON();
        json.confirmation_code = this.get_confirmation_code();
        json.mpesa_transaction_id = this.get_mpesa_transaction_id();
        return json;
    },

    get_confirmation_code() {
        const paymentLines = this.get_paymentlines();
        for (const line of paymentLines) {
            if (line.confirmation_code) {
                return line.confirmation_code;
            }
        }
        return null;
    },

    get_mpesa_transaction_id() {
        const paymentLines = this.get_paymentlines();
        for (const line of paymentLines) {
            if (line.mpesa_transaction_id) {
                return line.mpesa_transaction_id;
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
        this.rpc = useService("rpc");
        this.popup = useService("popup");
        this.state = useState({
            setIsLoading: false
        })

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/axios/1.7.2/axios.min.js")
        })
    },



    async validateOrder(isForceValidate) {
        if (!await this.checkPaymentMethods()) {
            return;
        }
        await this.sendConfirmationCodeToBackend();
        return super.validateOrder(isForceValidate);
    },

    async checkPaymentMethods() {
        const order = this.pos.get_order();
        const paymentLines = order.get_paymentlines();

        for (const line of paymentLines) {
            if (this.isMpesaPaymentMethod(line.payment_method) && !line.mpesa_transaction_id) {
                const isConfirmed = await this.handleMpesaPayment(line);
                if (!isConfirmed) {
                    return false;
                }
            }
        }
        return true;
    },

    isMpesaPaymentMethod(paymentMethod) {
        return paymentMethod.name.toLowerCase() === 'mpesa' || paymentMethod.use_payment_terminal === 'mpesa';
    },

    async handleMpesaPayment(paymentLine) {
        const { confirmed, payload: phoneNumber } = await this.popup.add(TextInputPopup, {
            title: _t("M-Pesa Payment"),
            body: _t("Enter customer's phone number:"),
            placeholder: _t("e.g., 254701044030"),
        });

        if (!confirmed) {
            this.pos.get_order().remove_paymentline(paymentLine);
            return false;
        }

        if (!this.validatePhoneNumber(phoneNumber)) {
            await this.showErrorPopup(_t("Invalid Phone Number"), _t("Please enter a valid Kenyan phone number starting with 254."));
            this.pos.get_order().remove_paymentline(paymentLine);
            return false;
        }

        try {
            const result = await this.initiateSTKPush(phoneNumber, paymentLine.amount);

            if (result.ResponseCode === "0") {
                paymentLine.mpesa_transaction_id = result.CheckoutRequestID;
                await this.showSuccessPopup(_t("M-Pesa Payment Initiated"), _t("Please check your phone to complete the payment."));
                return true;
            } else {
                await this.showErrorPopup(_t("M-Pesa Payment Failed"), result.ResponseDescription || _t("Unknown error occurred"));
                this.pos.get_order().remove_paymentline(paymentLine);
                return false;
            }
        } catch (error) {
            await this.showErrorPopup(_t("M-Pesa Payment Error"), error.message || _t("An unexpected error occurred. Please try again."));
            this.pos.get_order().remove_paymentline(paymentLine);
            return false;
        }
    },

    validatePhoneNumber(phoneNumber) {
        return /^254\d{9}$/.test(phoneNumber);
    },

    async initiateSTKPush(phoneNumber, amount) {
        // const order = this.pos.get_order();
        // const timestamp = this.getCurrentTimestamp();


        // const requestBody = {
        //     BusinessShortCode: this.pos.config.mpesa_shortcode,
        //     Password: this.generatePassword(timestamp),
        //     Timestamp: timestamp,
        //     TransactionType: "CustomerPayBillOnline",
        //     Amount: Math.round(amount),
        //     PartyA: phoneNumber,
        //     PartyB: this.pos.config.mpesa_shortcode,
        //     PhoneNumber: phoneNumber,
        //     CallBackURL: this.pos.config.mpesa_callback_url,
        //     AccountReference: order.name || "Order",
        //     TransactionDesc: `Payment for ${this.pos.config.name}`,
        // };

        // const headers = new Headers();
        // headers.append("Content-Type", "application/json");
        // headers.append("Authorization", `Bearer ${this.pos.config.mpesa_access_token}`);

        try {
            const response = await axios.post("https://mpesa-odoo-server.onrender.com/api/stkpush", {
                phone: phoneNumber,
                amount: amount.toString(), // Convert amount to string
            });
            // setTransactionDetails(data);
            console.log(response);
            setIsLoading(false);
            MpesaStkPushSuccess();
            await validateTransaction(response);
        } catch (error) {
            console.log(error);
            setIsLoading(false);
            MpesaStkPushFailed();
        }

    },

    getCurrentTimestamp() {
        const now = new Date();
        return now.toISOString().replace(/[^0-9]/g, "").slice(0, -3);
    },

    generatePassword(timestamp) {
        const passkey = this.pos.config.mpesa_passkey;
        const shortcode = this.pos.config.mpesa_shortcode;
        const str = `${shortcode}${passkey}${timestamp}`;
        return btoa(str);
    },

    async showSuccessPopup(title, body) {
        await this.popup.add('ConfirmPopup', { title, body });
    },

    async showErrorPopup(title, body) {
        await this.popup.add(ErrorPopup, { title, body });
    },

    async sendConfirmationCodeToBackend() {
        const order = this.pos.get_order();
        const confirmationCode = order.get_confirmation_code();
        const mpesaTransactionId = order.get_mpesa_transaction_id();

        if (confirmationCode || mpesaTransactionId) {
            try {
                const companyId = this.pos.config.company_id[0];
                await this.orm.call(
                    'pos.order',
                    'update_order_mpesa_details',
                    [order.name, confirmationCode, mpesaTransactionId],
                    { context: { company_id: companyId } }
                );
            } catch (error) {
                console.error("Error sending M-Pesa details to backend:", error);
                await this.showErrorPopup(_t('Backend Error'), _t('Failed to send M-Pesa details to the server. Please try again or contact support.'));
            }
        }
    },

    async testConnection() {
        try {
            const response = await fetch('https://httpbin.org/get');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Test connection successful:', data);
            return true;
        } catch (error) {
            console.error('Test connection failed:', error);
            return false;
        }
    },
});