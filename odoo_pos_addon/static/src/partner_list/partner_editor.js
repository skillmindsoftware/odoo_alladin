/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useState } from "@odoo/owl";

patch(PartnerDetailsEdit.prototype, {
    setup() {
        const res = super.setup(...arguments);

        this.popup = useService("popup");
        this.pos = usePos();
        this.intFields = ["country_id", "state_id", "property_product_pricelist"];
        const partner = this.props.partner;
        this.changes = useState({
            name: partner.name || "",
            street: partner.street || "",
            city: partner.city || "",
            zip: partner.zip || "",
            state_id: partner.state_id && partner.state_id[0],
            country_id: partner.country_id && partner.country_id[0],
            lang: partner.lang || "",
            email: partner.email || "",
            phone: partner.phone || "",
            mobile: partner.mobile || "",
            barcode: partner.barcode || "",
            vat: partner.vat || "",
            property_product_pricelist: this.setDefaultPricelist(partner),
        });
        // Provides translated terms used in the view
        this.partnerDetailsFields = {
            'Street': _t('Street'),
            'City': _t('City'),
            'Zip': _t('Zip'),
            'Email': _t('Email'),
            'Phone': _t('Phone'),
            'Mobile': _t('Mobile'),
            'Barcode': _t('Barcode')
        };
        Object.assign(this.props.imperativeHandle, {
            save: () => this.saveChanges(),
        });
    },

    saveChanges() {
        const processedChanges = { ...this.changes };
        console.log("changes saved");

        if ((!this.props.partner.email && !processedChanges.email) || processedChanges.email === "") {
            return this.popup.add(ErrorPopup, {
                title: _t("A Customer Email Is Required"),
            });
        }

        if ((!this.props.partner.phone && !processedChanges.phone) || processedChanges.phone === "") {
            return this.popup.add(ErrorPopup, {
                title: _t("A Customer Phone number Is Required"),
            });
        }

        if ((!this.props.partner.vat && !processedChanges.vat) || processedChanges.vat === "") {
            return this.popup.add(ErrorPopup, {
                title: _t("A Customer VAT Pin Is Required"),
            });
        }

        processedChanges.id = this.props.partner.id || false;
        this.props.saveChanges(processedChanges);

    },
});
