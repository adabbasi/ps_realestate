from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string="Property type", required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string="Total Offers" , compute="_compute_offer_count")
    _sql_constraints = [
        ('name', 'Unique(name)', 'No duplicate property types allowed')
         ]
    property_type_ids = fields.One2many('estate.property','property_type_id')


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
         rec.offer_count  = len(rec.offer_ids)
        return rec.offer_count

    def estate_offer_action(self):
        return {
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'context':{},
            'domain':[('property_type_id', '=', self.id)],
            'target':'current',
            'type': 'ir.actions.act_window'
        }