from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import csv
import xlrd
from io import StringIO
import logging
import os

_logger = logging.getLogger(__name__)


class CustomImportProduct(models.TransientModel):
    _name = "custom.import.product"
    _description = "Import Products with Variants"

    file_data = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="File Name")
    file_type = fields.Selection(
        [("csv", "CSV"), ("excel", "Excel")],
        string="File Type",
        required=True,
        default="csv",
    )

    def import_products(self):
        try:
            if self.file_type == "csv":
                rows = self._read_csv_file()
            else:
                rows = self._read_excel_file()

            if not rows:
                return self._create_error_message("No data found in the file.")

            success_count = 0
            errors = []

            for index, row in enumerate(rows, start=2):
                try:
                    self._validate_row(row)
                    self._process_row(row)
                    success_count += 1
                except Exception as e:
                    error_message = f"Row {index}: {str(e)}"
                    errors.append(error_message)
                    _logger.error(f"Error processing row: {row}. Error: {str(e)}")

            message = f"Import completed successfully. Products created/updated: {success_count}"
            if errors:
                message += (
                    f"\nErrors encountered: {len(errors)}. Check the logs for details."
                )

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": message,
                    "type": "success",
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }

        except Exception as e:
            return self._create_error_message(str(e))

    def _read_csv_file(self):
        try:
            csv_data = base64.b64decode(self.file_data).decode("utf-8")
            csv_file = StringIO(csv_data)
            reader = csv.DictReader(csv_file)
            return list(reader)
        except Exception as e:
            raise UserError(f"Error reading CSV file: {str(e)}")

    def _read_excel_file(self):
        try:
            excel_data = base64.b64decode(self.file_data)
            book = xlrd.open_workbook(file_contents=excel_data)
            sheet = book.sheet_by_index(0)
            headers = [cell.value for cell in sheet.row(0)]

            rows = []
            for i in range(1, sheet.nrows):
                row = {}
                for j, header in enumerate(headers):
                    row[header] = sheet.cell(i, j).value
                rows.append(row)

            return rows
        except Exception as e:
            raise UserError(f"Error reading Excel file: {str(e)}")

    def _validate_row(self, row):
        required_fields = [
            "vendor_sku",
            "Product Category",
            "POS Category",
            "Internal reference",
            "Name",
            "Size",
            "Color",
            "Cost",
            "Discount",
            "Sales Price",
        ]
        missing_fields = [field for field in required_fields if not row.get(field)]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    def _process_row(self, row):
        ProductTemplate = self.env["product.template"]
        ProductProduct = self.env["product.product"]
        ProductCategory = self.env["product.category"]
        ProductAttribute = self.env["product.attribute"]
        ProductAttributeValue = self.env["product.attribute.value"]

        # Find or create product category
        category = ProductCategory.search(
            [("name", "=", row["Product Category"])], limit=1
        )
        if not category:
            category = ProductCategory.create({"name": row["Product Category"]})

        # Find or create POS category
        pos_category = self.env["pos.category"].search(
            [("name", "=", row["POS Category"])], limit=1
        )
        if not pos_category:
            pos_category = self.env["pos.category"].create(
                {"name": row["POS Category"]}
            )

        # Find or create product template
        product_template = ProductTemplate.search([("name", "=", row["Name"])], limit=1)
        if not product_template:
            product_template = ProductTemplate.create(
                {
                    "name": row["Name"],
                    "type": "product",
                    "categ_id": category.id,
                    "pos_categ_id": pos_category.id,
                }
            )

        # Create or update attributes and values
        attribute_value_ids = []
        for attr_name in ["Size", "Color"]:
            attribute = ProductAttribute.search([("name", "=", attr_name)], limit=1)
            if not attribute:
                attribute = ProductAttribute.create({"name": attr_name})

            value = ProductAttributeValue.search(
                [("name", "=", row[attr_name]), ("attribute_id", "=", attribute.id)],
                limit=1,
            )
            if not value:
                value = ProductAttributeValue.create(
                    {"name": row[attr_name], "attribute_id": attribute.id}
                )

            attribute_value_ids.append(value.id)

            # Add attribute line to product template if not exists
            attr_line = product_template.attribute_line_ids.filtered(
                lambda l: l.attribute_id == attribute
            )
            if not attr_line:
                self.env["product.template.attribute.line"].create(
                    {
                        "product_tmpl_id": product_template.id,
                        "attribute_id": attribute.id,
                        "value_ids": [(4, value.id)],
                    }
                )
            elif value not in attr_line.value_ids:
                attr_line.write({"value_ids": [(4, value.id)]})

        # Find or create product variant
        domain = [
            ("product_tmpl_id", "=", product_template.id),
            (
                "product_template_attribute_value_ids.product_attribute_value_id",
                "in",
                attribute_value_ids,
            ),
        ]
        product_variant = ProductProduct.search(domain, limit=1)

        if not product_variant:
            # Create new variant
            product_variant = ProductProduct.create(
                {
                    "product_tmpl_id": product_template.id,
                    "default_code": row["Internal reference"],
                    "standard_price": float(row["Cost"]),
                }
            )
            _logger.info(f"Created new product variant: {product_variant.default_code}")
        else:
            # Update existing variant
            product_variant.write(
                {
                    "default_code": row["Internal reference"],
                    "standard_price": float(row["Cost"]),
                }
            )
            _logger.info(f"Updated product variant: {product_variant.default_code}")

        # Set variant attributes
        ptav_ids = (
            self.env["product.template.attribute.value"]
            .search(
                [
                    ("product_tmpl_id", "=", product_template.id),
                    ("product_attribute_value_id", "in", attribute_value_ids),
                ]
            )
            .ids
        )
        product_variant.product_template_attribute_value_ids = [(6, 0, ptav_ids)]

        # Set sales price for the variant
        self._set_variant_price(product_variant, float(row["Sales Price"]))

        # Handle discount
        if float(row["Discount"]) > 0:
            self._update_product_pricelist(product_variant, float(row["Discount"]))

    def _set_variant_price(self, product_variant, price):
        product_variant.lst_price = price

    def _update_product_pricelist(self, product_variant, discount):
        PricelistItem = self.env["product.pricelist.item"]
        Pricelist = self.env["product.pricelist"]

        default_pricelist = Pricelist.search(
            [("name", "=", "Public Pricelist")], limit=1
        )
        if not default_pricelist:
            default_pricelist = Pricelist.create(
                {
                    "name": "Public Pricelist",
                    "currency_id": self.env.company.currency_id.id,
                }
            )
            _logger.info(f"Created new pricelist: {default_pricelist.name}")

        pricelist_item = PricelistItem.search(
            [
                ("product_id", "=", product_variant.id),
                ("pricelist_id", "=", default_pricelist.id),
            ],
            limit=1,
        )

        if pricelist_item:
            pricelist_item.write({"percent_price": -discount})
        else:
            PricelistItem.create(
                {
                    "product_id": product_variant.id,
                    "pricelist_id": default_pricelist.id,
                    "compute_price": "percentage",
                    "percent_price": -discount,
                }
            )

    def _create_error_message(self, error_details):
        error_message = f"Failed to import file. Error: {error_details}"
        _logger.error(error_message)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": error_message,
                "type": "danger",
                "sticky": True,
            },
        }

    def download_template(self):
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(module_path, "data", "product_import_template.csv")

        if not os.path.exists(file_path):
            raise UserError(
                _("Template file not found. Please contact your administrator.")
            )

        with open(file_path, "rb") as file:
            file_content = file.read()

        encoded_content = base64.b64encode(file_content)

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/?model={self._name}&id={self.id}&field=file_data&filename_field=file_name&download=true",
            "target": "self",
        }

    def write(self, vals):
        res = super(CustomImportProduct, self).write(vals)
        if "file_data" in vals:
            self.file_name = "product_import_template.csv"
        return res
