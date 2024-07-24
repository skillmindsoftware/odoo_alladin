/** @odoo-module **/

import { PosStore } from '@point_of_sale/app/store/pos_store';
import { Order, Orderline } from '@point_of_sale/app/store/models';
import { patch } from '@web/core/utils/patch';

patch(PosStore.prototype, {
    async _processData(loadedData) {
        const result = await super._processData(...arguments);

        // Correct the typo: prodduct_by_id -> product_by_id
        // Also, add a check to ensure product_by_id exists and is iterable
        if (this.db && this.db.product_by_id && typeof this.db.product_by_id[Symbol.iterator] === 'function') {
            for (const product of this.db.product_by_id) {
                if (product) {
                    product.discount_rate = product.discount_rate || 0;
                }
            }
            console.log('Processed product data with discount_rate:', this.db.product_by_id);
        } else {
            console.warn('Unable to process product data: this.db.product_by_id is not iterable or undefined');
        }

        return result;
    },
});

patch(Orderline.prototype, {
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if (json.discount === undefined && this.product) {
            this.set_discount(this.product.discount_rate || 0);
            console.log(`Applied discount ${this.product.discount_rate || 0}% to product ${this.product.id}`);
        }
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (this.product && this.discount === 0) {
            json.discount = this.product.discount_rate || 0;
            console.log(`Exporting orderline with discount ${json.discount}% for product ${this.product.id}`);
        }
        return json;
    },
});

patch(Order.prototype, {
    add_product(product, options) {
        super.add_product(...arguments);
        const line = this.get_last_orderline();
        if (line && line.product && line.product.discount_rate > 0) {
            line.set_discount(line.product.discount_rate);
            console.log(`Set discount ${line.product.discount_rate}% for product ${line.product.id} in orderline`);
        }
    },
});
