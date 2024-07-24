// /** @odoo-module */

// import Registries from "point_of_sale.Registries"
// import { PosGlobalState } from "point_of_sale.models"

// const PosGlobalStateInherit = (models) => class extends models {
//     constructor(obj) {
//         super(obj);
//         console.log("Inherited PosGlobalState")
//         this.discounted_products = this.getProductDiscount()
//         this.popupMessage = ""
//     }


//     async getProductDiscount() {
//         const data = await this.env.services.rpc({
//             'model': 'product.product',
//             'method': 'getProductDiscount',
//             'args': [{}]
//         })

//         console.log("Discounted products", data)

//         return data
//     }

//     async setFavoriteProducts() {
//         this.discounted_products = await this.getProductDiscount()
//     }
// }

// Registries.Model.extend(PosGlobalState, PosGlobalStateInherit)