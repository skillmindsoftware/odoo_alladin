/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, xml } = owl;

class PopulateMoveLines extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
    }

    async populateMoveLines() {
        const { picking_id, available_stock } = this.props.action.params;
        
        await this.orm.create("stock.move", available_stock.map(item => ({
            name: item.product_name,
            product_id: item.product_id,
            product_uom_qty: item.quantity,
            product_uom: item.uom_id,
            picking_id: picking_id,
            location_id: this.props.action.context.default_location_id,
            location_dest_id: this.props.action.context.default_location_dest_id,
        })));

        this.action.doAction({
            type: 'ir.actions.client',
            tag: 'reload',
        });
    }
}

PopulateMoveLines.template = xml`
    <div t-on-click="populateMoveLines">
        <t t-esc="props.action.name"/>
    </div>
`;

registry.category("actions").add("populate_move_lines", PopulateMoveLines);